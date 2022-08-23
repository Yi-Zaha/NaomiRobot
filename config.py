
from os import environ

class Config(object):
        #Your telegram BOT API token : get it from @BotFather
        TOKEN = environ.get("TOKEN")
        #API_ID of your Telegram Account my.telegram.org/apps
        API_ID = int(environ.get("API_ID"))
        #API_HASH of your Telegram Account my.telegram.org/apps
        API_HASH = environ.get("API_HASH")
        #API_ID of your Telegram Account my.telegram.org/apps
        API_ID1 = int(environ.get("API_ID1"))
        #API_HASH of your Telegram Account my.telegram.org/apps
        API_HASH1 = environ.get("API_HASH1")
        #Your telegram user id
        OWNER_ID = environ.get("OWNER_ID")
        #For logs channel to note down important bot level events, recommend to make this public. ex: '-123456'
        LOG_GROUP_ID = environ.get("LOG_GROUP_ID")
        #Get From Here.https://www.mongodb.com/ (Same as MONGO_URL but give differant value for this) 
        BASE_DB = environ.get("BASE_DB")
        #Get From Here.https://www.mongodb.com/
        MONGO_DB_URI = environ.get("MONGO_DB_URI")
        #Don't change this value:https://arq.hamker.in
        ARQ_API_URL = environ.get("ARQ_API_URL")
        #Get this from @ARQRobot.
        ARQ_API_KEY = environ.get("ARQ_API_KEY")
        #now you can set custom command handler for rose like : / ! ,
        COMMAND_PREFIXES = "/"
        #The Telegram channel id you want focus user.(User can't start your bot without join it)
        F_SUB_CHANNEL = environ.get("F_SUB_CHANNEL")
