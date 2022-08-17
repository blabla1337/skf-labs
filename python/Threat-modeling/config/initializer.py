#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('../Database.db')

with con:
    
    cur = con.cursor()
    
    #Create data for the user table
    cur.execute("CREATE TABLE users(UserId INTEGER PRIMARY KEY AUTOINCREMENT, UserName TEXT, Password TEXT)")
    cur.execute("INSERT INTO users VALUES(1,'admin','admin')")
    cur.execute("INSERT INTO users VALUES(2,'user','user')")

    
    #Create some data for pageinformation
    cur.execute("CREATE TABLE notes(MessageId INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, Body TEXT, UserId INT)")
    cur.execute("INSERT INTO notes VALUES(1,'First note','This is a secret message that should not be shown to ordinary folks',1)")
    
    cur.execute("CREATE TABLE passwordForget(UserName TEXT, ResetToken TEXT)")

    con.commit()
    #con.close()
