# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
import os


def get_user_list(config, key):
    with open("{}/Naomi/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    ALLOW_EXCL=True
    API_HASH="c0da9c346d2c45dbc7ec49a05da9b2b6"
    API_ID=13675555
    ARQ_API_KEY="LJMETG-DPHBCX-DGHJCD-TMFIGB-ARQ"
    ARQ_API_URL="https://arq.hamker.in"
    BOT_ID=5548310123
    CASH_API_KEY="LUCXC3WOGJG5Z0VI"
    DATABASE_URL="postgres://bovnygnt:HbpZhz6T6Koeub6B-QfpgcIyYD4HpeZU@jelani.db.elephantsql.com/bovnygnt"
    ENV = "ANYTHING"
    EVENT_LOGS = -1001638398396
    JOIN_LOGGER = -1001638398396
    MONGO_DB_URI="mongodb+srv://raj1:raj1@cluster0.wtuav.mongodb.net/?retryWrites=true&w=majority"
    OWNER_ID=5591954930
    OWNER_USERNAME="cant_think_1"
    SPAMWATCH_API="RW8OiWPawUgvbZY1oH5UH5PsH5_kPMd6RUy7EAOSZrNKB5rufVGHvR3hfBnUHKh_"
    START_IMG="https://telegra.ph/file/755a979e1e5bfb6fc5c0b.jpg"
    SUPPORT_CHAT = "naomi_supp"
    TIME_API_KEY = "VZCX9WHJTKED"
    TOKEN = "5548310123:AAFD0VhhA0CIkn9v2Z24grg2bvIp_-_Zrs0"
    LOAD = []
    NO_LOAD = ["antinsfw", "cleaner"]
    WEBHOOK = False
    INFOPIC = True
    URL = None

    # OPTIONAL
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = ["5066050315"]
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = get_user_list("elevated_users.json", "supports")
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = get_user_list("elevated_users.json", "tigers")
    WOLVES = get_user_list("elevated_users.json", "whitelists")
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
