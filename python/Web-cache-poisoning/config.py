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
    CACHE_TYPE            = os.environ['CACHE_TYPE']
    CACHE_REDIS_HOST      = os.environ['CACHE_REDIS_HOST']
    CACHE_REDIS_PORT      = os.environ['CACHE_REDIS_PORT']
    CACHE_REDIS_DB        = os.environ['CACHE_REDIS_DB']
    CACHE_REDIS_URL       = os.environ['CACHE_REDIS_URL']
    CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
    ATTACK_SERVER_HOST    = os.environ['ATTACK_SERVER_HOST']
    ATTACK_SERVER_PORT    = os.environ['ATTACK_SERVER_PORT']
    ATTACK_SERVER_URL     = os.environ['ATTACK_SERVER_URL']
    # CACHE_TYPE            = 'SimpleCache'
    # CACHE_DEFAULT_TIMEOUT = 3
    # ATTACK_SERVER_URL     = 'localhost'
