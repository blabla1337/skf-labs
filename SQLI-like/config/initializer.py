#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('Database.db')

with con:
    
    cur = con.cursor()
    
    #Create data for the user table
    cur.execute("CREATE TABLE users(UserId INT, UserName TEXT, Password TEXT, email TEXT)")
    cur.execute("INSERT INTO users VALUES(1,'Admin','0cef1fb10f60529028a71f58e54ed07b', 'admin@foobar.com')")
    cur.execute("INSERT INTO users VALUES(2,'User','022b5ac7ea72a5ee3bfc6b3eb461f2fc', 'user@lala.com')")
    cur.execute("INSERT INTO users VALUES(3,'Guest','94ca112be7fc3f3934c45c6809875168', 'guest@localhost')")
    cur.execute("INSERT INTO users VALUES(4,'Plebian','0cbdc7572ff7d07cc6807a5b102a3b93', 'plebian@bla.org')")
    
    con.commit()
    #con.close()
