#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('Database.db')

with con:
    
    cur = con.cursor()
    
    #Create data for the user table
    cur.execute("CREATE TABLE users(UserId INT, UserName TEXT, Password TEXT)")
    cur.execute("INSERT INTO users VALUES(1,'admin','admin')")

    #Create some data for pageinformation
    cur.execute("CREATE TABLE prefs_users(PreferenceId INT, API_key TEXT, UserId)")
    cur.execute("INSERT INTO prefs_users VALUES(1,'5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', 1)")
    cur.execute("INSERT INTO prefs_users VALUES(1,'cbfdac6008f9cab4083784cbd1874f76618d2a97', 1)")

    con.commit()
    #con.close()
