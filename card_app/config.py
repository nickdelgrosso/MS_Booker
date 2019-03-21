import os

class BaseConfig:
    SECRET_KEY = 'change me later!'  # todo: hide secret key.
    PROJECTDB_USER = os.getenv('PROJECTDB_USER')
    PROJECTDB_PASSWD = os.getenv('PROJECTDB_PASSWD')
    PROJECTDB_URL = os.getenv('PROJECTDB_URL')
    if not all([PROJECTDB_PASSWD, PROJECTDB_USER, PROJECTDB_URL]):
        raise ValueError("PROJECTDB Environment Variables must be Set!")