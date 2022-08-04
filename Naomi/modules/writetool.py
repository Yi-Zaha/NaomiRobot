import requests
from requests import get
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from Naomi import pbot, dispatcher, SUPPORT_CHAT


@pbot.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        name = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1].replace(" ", "%20")
        )
        m = await pbot.send_message(
            message.chat.id, "**ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ...**"
        )
        photo = "https://apis.xditya.me/write?text=" + name
        caption = f"""
✨ **ᴡʀɪᴛᴛᴇɴ ʙʏ :** [{dispatcher.bot.first_name}](https://t.me/{dispatcher.bot.username})
"""
        await pbot.send_photo(
            message.chat.id,
            photo=photo,
            caption=caption,)
        await m.delete()
    else:
        lol = message.reply_to_message.text
        name = lol.split(None, 0)[0].replace(" ", "%20")
        m = await pbot.send_message(
            message.chat.id, "**ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ..."
        )
        photo = "https://apis.xditya.me/write?text=" + name
        caption = f""" 💫**ᴡʀɪᴛᴛᴇɴ ʙʏ :** [{dispatcher.bot.first_name}](https://t.me/{dispatcher.bot.username})"""
        await pbot.send_photo(
            message.chat.id,
            photo=photo,
            caption=caption,
        )
        await m.delete()
