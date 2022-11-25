import logging
import os
import sys
import time
import json

import telegram.ext as tg
from aiohttp import ClientSession
from pyrogram import Client, errors
from Python_ARQ import ARQ
from telethon import TelegramClient


def get_user_list(config, key):
    with open("{}/Naomi/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = set(int(x) for x in os.environ.get("DRAGONS", "").split())
        DEV_USERS = set(int(x) for x in os.environ.get("DEV_USERS", "").split())
    except ValueError:
        raise Exception("Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = set(int(x) for x in os.environ.get("DEMONS", "").split())
    except ValueError:
        raise Exception("Your support users list does not contain valid integers.")

    try:
        WOLVES = set(int(x) for x in os.environ.get("WOLVES", "").split())
    except ValueError:
        raise Exception("Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = set(int(x) for x in os.environ.get("TIGERS", "").split())
    except ValueError:
        raise Exception("Your tiger users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get("INFOPIC", "True"))
    START_IMG = os.environ.get("START_IMG", None)
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get("API_ID", None)
    API_HASH = os.environ.get("API_HASH", None)

    DB_URI = os.environ.get("DATABASE_URL")
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    DONATION_LINK = os.environ.get("DONATION_LINK")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)
    CASH_API_KEY = os.environ.get("CASH_API_KEY", None)
    TIME_API_KEY = os.environ.get("TIME_API_KEY", None)
    SUPPORT_CHAT = os.environ.get("SUPPORT_CHAT", None)
    ARQ_API_URL = os.environ.get("ARQ_API_URL", "https://arq.hamker.in")
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", "LJMETG-DPHBCX-DGHJCD-TMFIGB-ARQ")

    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)

    try:
        BL_CHATS = set(int(x) for x in os.environ.get("BL_CHATS", "").split())
    except ValueError:
        raise Exception("Your blacklisted chats list does not contain valid integers.")

else:
     ALLOW_EXCL= True
     API_HASH="c0da9c346d2c45dbc7ec49a05da9b2b6"
     API_ID=13675555
     ARQ_API_KEY="LJMETG-DPHBCX-DGHJCD-TMFIGB-ARQ"
     ARQ_API_URL="https://arq.hamker.in"
     BOT_ID=5548310123
     CASH_API_KEY="LUCXC3WOGJG5Z0VI"
     DB_URI="postgres://mqivcxqxbgejsm:de62039a0e705a3b7b12b15fa4d70ca493ca5313000a058f281976a14e7eea41@ec2-3-219-229-143.compute-1.amazonaws.com:5432/d4atecmlssb82m"
     ENV="ANYTHING"
     EVENT_LOGS=-1001638398396
     JOIN_LOGGER=-1001638398396
     MONGO_DB_URI="mongodb+srv://raj1:raj1@cluster0.wtuav.mongodb.net/?retryWrites=true&w=majority"
     NO_LOAD="antinsfw"
     OWNER_ID="5591954930"
     OWNER_USERNAME="cant_think_1"
     SPAMWATCH_API="RW8OiWPawUgvbZY1oH5UH5PsH5_kPMd6RUy7EAOSZrNKB5rufVGHvR3hfBnUHKh_"
     START_IMG="https://telegra.ph/file/755a979e1e5bfb6fc5c0b.jpg"
     SUPPORT_CHAT="naomi_supp"
     TIME_API_KEY="VZCX9WHJTKED"
     TOKEN="5555986769:AAEVhk7pXR8SlJA_OZMPxon-gsB-IOK-7MQ"
     SPAMMERS = None
     ALLOW_CHATS = True
     HEROKU_API_KEY = None
     HEROKU_APP_NAME = None
     TEMP_DOWNLOAD_DIRECTORY = "./"
     BL_CHATS = []  # List of groups that you want blacklisted.
     LOAD = []
     BAN_STICKER = ("CAACAgUAAxkBAAEDafNhq5Z0DegqVzauwSighMw5cPWp8QACVgQAAuUG0FRXfCEuBziNzCIE")
     WORKERS = 8
     DONATION_LINK = ""
     CERT_PATH = None
     PORT = 5000
     DEL_CMDS = True
     STRICT_GBAN = True
     DRAGONS = get_user_list("elevated_users.json", "sudos")
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
     DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
     DEMONS = get_user_list("elevated_users.json", "supports")
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
     TIGERS = get_user_list("elevated_users.json", "tigers")
     WOLVES = get_user_list("elevated_users.json", "whitelists")
     URL = None
     INFOPIC = True
     try:
         BL_CHATS = set(int(x) for x in BL_CHATS or [])
     except ValueError:
         raise Exception("Your blacklisted chats list does not contain valid integers.")


updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)
telethn = TelegramClient("Naomi", API_ID, API_HASH)

pbot = Client("Naomirobot", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()

# Bot info
print("[INFO]: Getting Bot Info...")
BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username

# ARQ Client
print("[INFO]: INITIALIZING ARQ CLIENT...")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from Naomi.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler
