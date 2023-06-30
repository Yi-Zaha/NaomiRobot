import asyncio
import sys
import logging
from motor import motor_asyncio
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from Naomi.confing import get_int_key, get_str_key

MONGO_DB_URI="mongodb+srv://f2l:f2l@cluster0.fjjge1y.mongodb.net/?retryWrites=true&w=majority"
MONGO_PORT = 27017
MONGO_DB = "f2l"


client = MongoClient()
client = MongoClient(MONGO_DB_URI, MONGO_PORT)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI, MONGO_PORT)
db = motor[MONGO_DB]
db = client["raj"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(logging.critical("Can't connect to mongodb! Exiting..."))
