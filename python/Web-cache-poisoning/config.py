import os

class Config(object):
    CACHE_TYPE            = "redis"
    CACHE_REDIS_HOST      = "localhost"
    CACHE_REDIS_PORT      = 6379
    CACHE_REDIS_DB        = 0
    CACHE_REDIS_URL       = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300
    # CACHE_TYPE            = 'SimpleCache'
    # CACHE_DEFAULT_TIMEOUT = 3
    # ATTACK_SERVER_URL     = 'localhost'
