
from os import environ

class Config(object):
        #Your telegram BOT API token : get it from @BotFather
        TOKEN = environ.get("TOKEN")
        #API_ID of your Telegram Account my.telegram.org/apps
        API_ID = int(environ.get("API_ID"))
        #API_HASH of your Telegram Account my.telegram.org/apps
        API_HASH = environ.get("API_HASH")
        OWNER_ID = environ.get("OWNER_ID")
        MONGO_DB_URI = environ.get("MONGO_DB_URI")
        #Don't change this value:https://arq.hamker.in
        ARQ_API_URL = environ.get("ARQ_API_URL")
        #Get this from @ARQRobot.
        ARQ_API_KEY = environ.get("ARQ_API_KEY")
        #now you can set custom command handler for rose like : / ! ,
        COMMAND_PREFIXES = "/"
