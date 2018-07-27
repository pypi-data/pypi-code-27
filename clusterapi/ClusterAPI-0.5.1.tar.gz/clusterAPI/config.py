
import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'cluster_api_key')
    ROOT_URL = '/api/v1'
    HOST = '0.0.0.0'
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 3000
    
    CIB_CMD = '/usr/sbin/cibadmin'
    CIB_CMD_OPTIONS = '-Q -l'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    AUTH_TOKEN_EXPIRY_DAYS = 100
    AUTH_TOKEN_EXPIRY_SECONDS = 120


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    AUTH_TOKEN_EXPIRY_DAYS = 0
    AUTH_TOKEN_EXPIRY_SECONDS = 3


class ProductionConfig(BaseConfig):
    DEBUG = True
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 20
