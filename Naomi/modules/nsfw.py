import html
import time
import requests
from pyrogram import filters
import nekos
from Naomi.utils.hmfull.src import hmfull
from Naomi import dispatcher, pbot, SUPPORT_CHAT
import Naomi.modules.sql1.nsfw_sql as sql
from Naomi.modules.log_channel import gloggable
from telegram import Update
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import CommandHandler, CallbackContext, run_async
from Naomi.modules.helper_funcs.filters import CustomFilters
from Naomi.modules.helper_funcs.chat_status import user_admin
from telegram.utils.helpers import mention_html
url_nsfw = "https://api.waifu.pics/nsfw/"

@user_admin
@gloggable
def add_nsfw(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    is_nsfw = sql.is_nsfw(chat.id)
    if not is_nsfw:
        sql.set_nsfw(chat.id)
        msg.reply_text("Activated NSFW Mode!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"ACTIVATED_NSFW\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message
    else:
        msg.reply_text("NSFW Mode is already Activated for this chat!")
        return ""

@user_admin
@gloggable
def rem_nsfw(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    is_nsfw = sql.is_nsfw(chat.id)
    if not is_nsfw:
        msg.reply_text("NSFW Mode is already Deactivated")
        return ""
    else:
        sql.rem_nsfw(chat.id)
        msg.reply_text("Rolled Back to SFW Mode!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"DEACTIVATED_NSFW\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message

def blowjob(update, context):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            msg.reply_text("NSFW is not activated!!\n\nUse '/addnsfw' to activate NSFW commands.")
            return
    url = f"{url_nsfw}blowjob" 
    result = requests.get(url).json()
    img = result['url']
    msg.reply_animation(img)

def trap(update, context):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            msg.reply_text("NSFW is not activated!!\n\nUse '/addnsfw' to activate NSFW commands.")
            return
    url = f"{url_nsfw}trap" 
    result = requests.get(url).json()
    img = result['url']
    msg.reply_photo(photo=img)

def nsfwwaifu(update, context):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            msg.reply_text("NSFW is not activated!!\n\nUse '/addnsfw' to activate NSFW commands.")
            return
    url = f"{url_nsfw}waifu" 
    result = requests.get(url).json()
    img = result['url']
    msg.reply_photo(photo=img)

def nsfwneko(update, context):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            msg.reply_text("NSFW is not activated!!\n\nUse '/addnsfw' to activate NSFW commands.")
            return
    url = f"{url_nsfw}neko" 
    result = requests.get(url).json()
    img = result['url']
    msg.reply_photo(photo=img)

def spank(update, context):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    if not update.effective_message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            return
    target = "spank"
    msg.reply_animation(nekos.img(target))


nsfw_query = ["ass", "cum", "creampie", "doujin", "blowjob", "bj", "boobjob", "vagina", "uniform", "foot", "femdom", "gangbang", "hentai", "incest", "ahegao", "gif", "ero", "cuckold", "orgy", "elves", "pantsu", "mobile", "glasses", "tentacles", "tentacle", "thighs", "yuri", "zettai", "masturbation", "public", "wlewd", "nekolewd", "nekogif", "henti", "hass", "boobs", "paizuri", "hyuri", "hthigh", "midriff", "kitsune", "tentacle", "anal", "hanal", "hneko"]
@pbot.on_message(filters.command(nsfw_query))
async def ass(_, message):
    chat_id = message.chat.id
    if not message.chat.type == "private":
        is_nsfw = sql.is_nsfw(chat_id)
        if not is_nsfw:
            await message.reply_text("NSFW is not activated!!\n\nUse '/addnsfw' to activate NSFW commands.")
            return
    query = message.text.split(" ")[0].replace("/", "")
    query = query.lower()
    try:
        if query in nsfw_query: 
            if query == "ass":
                res = hmfull.HMtai.nsfw.ass()
            elif query == "cum":
                res = hmfull.HMtai.nsfw.cum()
            elif query == "creampie":
                res = hmfull.HMtai.nsfw.creampie()
            elif query == "doujin":
                res = hmfull.HMtai.nsfw.manga()
            elif query == "blowjob" or query =="bj":
                res = hmfull.HMtai.nsfw.blowjob()
            elif query == "boobjob":
                res = hmfull.HMtai.nsfw.boobjob()
            elif query == "vagina":
                res = hmfull.HMtai.nsfw.vagina()
            elif query == "uniform":
                res = hmfull.HMtai.nsfw.uniform()
            elif query == "foot":
                res = hmfull.HMtai.nsfw.foot()
            elif query == "femdom":
                res = hmfull.HMtai.nsfw.femdom()
            elif query == "gangbang":
                res = hmfull.HMtai.nsfw.gangbang()
            elif query == "hentai":
                res = hmfull.HMtai.nsfw.hentai()
            elif query == "incest":
                res = hmfull.HMtai.nsfw.incest()
            elif query == "ahegao":
                res = hmfull.HMtai.nsfw.ahegao()
            elif query == "nekolewd":
                res = hmfull.HMtai.nsfw.neko()
            elif query == "gif":
                hmm = hmfull.HMtai.nsfw.gif()
                url = hmm["url"]
                return await message.reply_animation(url)
            elif query == "ero":
                res = hmfull.HMtai.nsfw.ero()
            elif query == "cuckold":
                res = hmfull.HMtai.nsfw.cuckold()
            elif query == "orgy":
                res = hmfull.HMtai.nsfw.orgy()
            elif query == "elves":
                res = hmfull.HMtai.nsfw.elves()
            elif query == "pantsu":
                res = hmfull.HMtai.nsfw.pantsu()
            elif query == "mobile":
                res = hmfull.HMtai.nsfw.nsfwMobileWallpaper()
            elif query == "glasses":
                res = hmfull.HMtai.nsfw.glasses()
            elif query == "tentacles":
                res = hmfull.HMtai.nsfw.tentacles()
            elif query == "thighs":
                res = hmfull.HMtai.nsfw.thighs()
            elif query == "yuri":
                res = hmfull.HMtai.nsfw.yuri()
            elif query == "zettai":
                res = hmfull.HMtai.nsfw.zettaiRyouiki()
            elif query == "masturbation":
                res = hmfull.HMtai.nsfw.masturbation()
            elif query == "public":
                res = hmfull.HMtai.nsfw.public()
            elif query == "wlewd":
                res = hmfull.Nekos.nsfw.wallpaper()
            elif query == "nekogif":
                hmm = hmfull.Nekos.nsfw.nekogif()
                url = hmm["url"]
                return await message.reply_animation(url)
            elif query == "henti":
                res = hmfull.NekoBot.nsfw.hentai()
            elif query == "hass":
                res = hmfull.NekoBot.nsfw.hass()
            elif query == "boobs":
                res = hmfull.NekoBot.nsfw.boobs()
            elif query == "paizuri":
                res = hmfull.NekoBot.nsfw.paizuri()
            elif query == "hyuri":
                res = hmfull.NekoBot.nsfw.yuri()
            elif query == "hthigh":
                res = hmfull.NekoBot.nsfw.thigh()
            elif query == "midriff":
                res = hmfull.NekoBot.nsfw.midriff()
            elif query == "kitsune":
                res = hmfull.NekoBot.nsfw.kitsune()
            elif query == "tentacle":
                res = hmfull.NekoBot.nsfw.tentacle()
            elif query == "anal":
                res = hmfull.NekoBot.nsfw.anal()
            elif query == "hanal":
                res = hmfull.NekoBot.nsfw.hanal()
            elif query == "hneko":
                res = hmfull.NekoBot.nsfw.hneko()

            url = res["url"]
            return await message.reply_photo(url)
    except:
        return await message.reply_text(f"ERROR!!! Contact @{SUPPORT_CHAT}")
    
    
__mod_name__ = "🇳sғᴡ"

__help__ = """
❍ `/addnsfw` : To Activate NSFW commands.
❍ `/rmnsfw` : To Deactivate NSFW commands.
*NSFW commands:*
 `/ass`
 `/bdsm`
 `/cum` 
 `/creampie` 
 `/doijin`
 `/blowjob`
 `/bj`
 `/boobjob`
 `/vagina`
 `/uniform`
 `/foot`
 `/femdom`
 `/gangbang` 
 `/hentai`
 `/incest`
 `/ahegao`
 `/neko`
 `/gif`
 `/ero`
 `/cuckold`
 `/orgy`
 `/elves`
 `/pantsu`
 `/mobile`
 `/glasses`
 `/tentacles`
 `/tentacle`
 `/thighs`
 `/yuri`
 `/zettai`
 `/masturbation`
 `/public`
 `/wlewd`
 `/nekolewd`
 `/nekogif`
 `/henti`
 `/hass`
 `/boobs`
 `/paizuri`
 `/hyuri`
 `/hthigh`
 `/midriff`
 `/kitsune`
 `/tentacle`
 `/anal`
 `/hanal`
 `/hneko`
 `/nsfwwaifu`
 `/blowjob`
 `/nwaifu`
 `/bj`
 `/trap`
 `/nsfwneko`
 `/nneko`
 `/spank`
"""
ADD_NSFW_HANDLER = CommandHandler("addnsfw", add_nsfw)
REMOVE_NSFW_HANDLER = CommandHandler("rmnsfw", rem_nsfw)
NSFWWAIFU_HANDLER = CommandHandler(["nsfwwaifu", "nwaifu"], nsfwwaifu)
BLOWJOB_HANDLER = CommandHandler(["blowjob", "bj"], blowjob)
TRAP_HANDLER = CommandHandler("trap", trap)
NSFWNEKO_HANDLER = CommandHandler(["nsfwneko", "nneko"], nsfwneko)
SPANK_HANDLER = CommandHandler("spank", spank)

dispatcher.add_handler(ADD_NSFW_HANDLER)
dispatcher.add_handler(REMOVE_NSFW_HANDLER)
dispatcher.add_handler(NSFWWAIFU_HANDLER)
dispatcher.add_handler(BLOWJOB_HANDLER)
dispatcher.add_handler(SPANK_HANDLER)
dispatcher.add_handler(TRAP_HANDLER)
dispatcher.add_handler(NSFWNEKO_HANDLER)

__handlers__ = [
    ADD_NSFW_HANDLER,
    REMOVE_NSFW_HANDLER,
    NSFWWAIFU_HANDLER,
    SPANK_HANDLER,
    BLOWJOB_HANDLER,
    TRAP_HANDLER,
    NSFWNEKO_HANDLER
]
