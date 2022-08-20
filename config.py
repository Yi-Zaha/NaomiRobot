"""Importing"""
from os import environ


class Config(object):
    API_ID = int(environ.get("API_ID", 0))
    API_HASH = environ.get("API_HASH", "")
    TOKEN = environ.get("TOKEN", "")
    MONGO_DB_URI = environ.get("MONGO_DB_URI", "")
