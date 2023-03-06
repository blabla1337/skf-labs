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

class Config(object):
    BACKEND_SERVER_1 = os.environ['BACKEND_SERVER_1']
    # BACKEND_SERVER_1 = "http://127.0.0.1:8081/"
