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
