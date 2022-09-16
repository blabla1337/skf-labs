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
# Description:
#   Create fresh database including sample data.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 

import sqlite3

DB_FILE_NAME = 'Database.db'

def initialize():
    with sqlite3.connect(DB_FILE_NAME) as connection:
        cursor = connection.cursor()

        # Create data for the users table. Use MD5 as hashing algorithm.
        cursor.execute("CREATE TABLE Users(UserId INT, username TEXT, hash TEXT)")
        cursor.execute("INSERT INTO Users VALUES(1,'admin','c7f96bc2560a7b9a9e9e52573fda3246')") # ADmiN!@#$SupErSaFE
        cursor.execute("INSERT INTO Users VALUES(2,'john','81dc9bdb52d04dc20036dbd8313ed055')") # 1234

        connection.commit()

if __name__ == '__main__':
    initialize()
