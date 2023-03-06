#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# SKF Labs - Security Knowledge Framework (SKF)
# Copyright (C) 2022, OWASP Foundation, Inc.
#
# This software is provided under a slightly modified version
# of The GNU Affero General Public License. See the accompanying LICENSE 
# file for more information.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 

import sqlite3

conn = sqlite3.connect('database.db')
print('Opened database successfully')

conn.execute('''CREATE TABLE users
         (ID INT PRIMARY KEY     NOT NULL,
          USERNAME       TEXT    NOT NULL,
          PASSWORD TEXT NOT NULL);''')
conn.execute('''CREATE TABLE "products" (
	"ID"	INTEGER NOT NULL UNIQUE,
	"TITLE"	TEXT NOT NULL UNIQUE,
	"NAME"	TEXT NOT NULL,
	"SALARY"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("ID" AUTOINCREMENT)
);''')
print('Tables created successfully')

conn.execute("INSERT INTO users (ID,USERNAME,PASSWORD) \
      VALUES (1, 'admin','Super@Complex$Password123#You%Never&Guess')")
conn.execute("INSERT INTO products (ID,TITLE,NAME,SALARY) \
      VALUES (0, 'CEO','Mr Mark Oney', 1000000)")
conn.execute("INSERT INTO products (ID,TITLE,NAME,SALARY) \
      VALUES (1, 'CIO','Ms Cristha Ash', 3000000)")
conn.execute("INSERT INTO products (ID,TITLE,NAME,SALARY) \
      VALUES (2, 'Stockholder','Mr Gary Old', 50000000)")
conn.commit()
print('Records created successfully')

command = 'SELECT USERNAME,PASSWORD from users'
result = conn.execute(command)
for row in result:
    username = row
    print(username)
conn.close()
