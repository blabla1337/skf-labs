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
#   Database layer functionalities including:
#       - User credential validation
#
# Author:
#   Alex Romero (@NtAlexio2)
# 

from config.sqlite import *
import hashlib

class DataAccess:

    def validateCredentials(self, username, password):
        hash = hashlib.md5(password.encode()).hexdigest().lower()
        connection = create_db_connection()
        cursor = connection.execute('SELECT username, hash FROM Users WHERE username=? AND hash=?', (username, hash, ))
        return cursor.fetchone() is not None

    def checkUserExists(self, username):
        connection = create_db_connection()
        cursor = connection.execute('SELECT username FROM Users WHERE username=?', (username, ))
        return cursor.fetchone() is not None

    def isAdmin(self, username):
        connection = create_db_connection()
        cursor = connection.execute('SELECT is_admin FROM Users WHERE username=?', (username, ))
        return bool(cursor.fetchone()[0])
