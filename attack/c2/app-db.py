#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error

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


