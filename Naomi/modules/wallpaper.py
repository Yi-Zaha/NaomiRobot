
import os
import io
import requests
from requests import get
from pyrogram.types import Message
from Naomi import pbot, dispatcher, SUPPORT_CHAT
from bs4 import *
from pyrogram import filters
from PIL import Image
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@pbot.on_message(filters.command(["wall", "wallpaper"]))
async def wall(client, message):
    quew = get_text(message)
    if not quew:
        await client.send_message(
            message.chat.id, "**ᴩʟᴇᴀsᴇ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ sᴇᴀʀᴄʜ ғᴏʀ ᴡᴀʟʟᴩᴀᴩᴇʀ !**"
        )
        return
    m = await client.send_message(message.chat.id, "⚙**sᴇᴀʀᴄʜɪɴɢ...**")
    try:
        text = get_text(message)
        LOGO_API = f"https://single-developers.up.railway.app/wallpaper?search={text}"
        randc = LOGO_API
        murl = (
            requests.get(
                f"https://single-developers.up.railway.app/wallpaper?search={text}"
            )
            .history[1]
            .url
        )
        img = Image.open(io.BytesIO(requests.get(randc).content))
        fname = "Naomi.png"
        img.save(fname, "png")
        caption = f"""
**By :** [{dispatcher.bot.first_name}](https://t.me/{dispatcher.bot.username})
"""
        await m.delete()
        await client.send_photo(
            message.chat.id,
            photo=murl,
            caption=caption,
        )
        if os.path.exists(fname):
            os.remove(fname)
    except Exception as e:
        await client.send_message(
            message.chat.id,
            f"sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ.\nᴩʟᴇᴀsᴇ ʀᴇᴩᴏʀᴛ ᴛʜɪs ᴀᴛ @{SUPPORT_CHAT}\n\n**ᴇʀʀᴏʀ :** {e}",
        )
