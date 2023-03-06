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

import sqlite3 as lite

con = lite.connect('Database.db')

with con:
    
    cur = con.cursor()
    
    #Create data for the user table
    cur.execute("CREATE TABLE users(UserId INT, UserName TEXT, Password TEXT)")
    cur.execute("INSERT INTO users VALUES(1,'admin','admin')")

    
    #Create some data for pageinformation
    cur.execute("CREATE TABLE prefs(PreferenceId INT, Color TEXT, UserId)")
    cur.execute("INSERT INTO prefs VALUES(1,'RED', 1)")
    
    con.commit()
    #con.close()
