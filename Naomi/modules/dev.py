import os
import subprocess
import sys

from contextlib import suppress
from time import sleep

import Naomi

from Naomi import dispatcher
from Naomi.modules.helper_funcs.chat_status import dev_plus
from telegram import TelegramError, Update
from telegram.error import Unauthorized
from telegram.ext import CallbackContext, CommandHandler, run_async


@run_async
@dev_plus
def allow_groups(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        update.effective_message.reply_text(f"Current state: {FallenRobot.ALLOW_CHATS}")
        return
    if args[0].lower() in ["off", "no"]:
        FallenRobot.ALLOW_CHATS = True
    elif args[0].lower() in ["yes", "on"]:
        FallenRobot.ALLOW_CHATS = False
    else:
        update.effective_message.reply_text("Format: /lockdown Yes/No or Off/On")
        return
    update.effective_message.reply_text("Done! Lockdown value toggled.")


@run_async
@dev_plus
def leave(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
        except TelegramError:
            update.effective_message.reply_text(
                "Beep boop, I could not leave that group(dunno why tho)."
            )
            return
        with suppress(Unauthorized):
            update.effective_message.reply_text("Beep boop, I left that soup!.")
    else:
        update.effective_message.reply_text("Send a valid chat ID")


@run_async
@dev_plus
def gitpull(update: Update, context: CallbackContext):
    sent_msg = update.effective_message.reply_text(
        "Pulling all changes from remote and then attempting to restart."
    )
    subprocess.Popen("git pull", stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\nChanges pulled...I guess.. Restarting in "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("Restarted.")

    os.system("restart.bat")
    os.execv("start.bat", sys.argv)


@run_async
@dev_plus
def restart(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "Starting a new instance and shutting down this one"
    )

    os.system("git pull -f -q")
    os.execl(sys.executable, sys.executable, "-m", "Naomi")


LEAVE_HANDLER = CommandHandler("leave", leave)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull)
RESTART_HANDLER = CommandHandler("reboot", restart)
ALLOWGROUPS_HANDLER = CommandHandler("lockdown", allow_groups)

dispatcher.add_handler(ALLOWGROUPS_HANDLER)
dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__mod_name__ = "🇩ᴇᴠ"
__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER, ALLOWGROUPS_HANDLER]
__command_list__ = ["leave", "gitpull", "reboot", "lockdown"]
__help__="""
*Broadcast: (Bot owner only)*
*Note:* This supports basic markdown
 ❍ /broadcastall*:* Broadcasts everywhere
 ❍ /broadcastusers*:* Broadcasts too all users
 ❍ /broadcastgroups*:* Broadcasts too all groups

*Masha Core* (Owner only)
 ❍ /send*:* <module name>*:* Send module
 ❍ /install*:* <reply to a .py>*:* Install module
 
*Heroku Settings* (Owner only)
 ❍ /usage*:* Check your heroku dyno hours remaining.
 ❍ /see var <var>*:* Get your existing varibles, use it only on your private group!
 ❍ /set var <newvar> <vavariable>*:* Add new variable or update existing value variable.
 ❍ /del var <var>*:* Delete existing variable.
 ❍ /logs Get heroku dyno logs.

*Windows self hosted only:*
 ❍ /reboot*:* Restarts the bots service
 ❍ /gitpull*:* Pulls the repo and then restarts the bots service

*Groups Info:*
 ❍ /groups*:* List the groups with Name, ID, members count as a txt
 ❍ /leave <ID>*:* Leave the group, ID must have hyphen
 ❍ /stats*:* Shows overall bot stats
 ❍ /getchats*:* Gets a list of group names the user has been seen in. Bot owner only
 ❍ /ginfo username/link/ID*:* Pulls info panel for entire group
"""
