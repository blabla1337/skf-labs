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
#   This file contains single function to return database connection.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 

from os import path
import sqlite3

DB_FILE_NAME = 'Database.db'

def create_db_connection():
    BASE_DIR = path.dirname(path.abspath(path.dirname(__file__)))
    db_path = path.join(BASE_DIR, DB_FILE_NAME)
    with sqlite3.connect(db_path) as connection:
        _ = connection.cursor()
    return connection
