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
    cur.execute("CREATE TABLE prefs(PreferenceId INT, Message TEXT, UserId)")
    cur.execute("INSERT INTO prefs VALUES(1,'RED', 1)")
    
    con.commit()
    #con.close()
