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

import os
import sqlite3

def database_con():
    BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    db_path = os.path.join(BASE_DIR, "Database.db")
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
    return con