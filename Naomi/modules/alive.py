import os
import re
import random
from pyrogram import Client, filters
from platform import python_version as kontol
from telethon import events, Button
from telegram import __version__ as telever
from telethon import __version__ as tlhver
from pyrogram import __version__ as pyrover
from Naomi.events import register
from Naomi import telethn as tbot, SUPPORT_CHAT, OWNER_USERNAME, dispatcher,pbot as app


PHOTO = [
    "https://telegra.ph/file/4f66f78c620693de0bb42.jpg",
    "https://telegra.ph/file/4f66f78c620693de0bb42.jpg",
]

@app.on_message(filters.command("start") & filters.group & ~filters.private)
async def awake(event):
    TEXT = f"**ʜᴇʏ​ [{event.sender.first_name}](tg://user?id={event.sender.id}),\n\nɪ ᴀᴍ {dispatcher.bot.first_name}**\n━━━━━━━━━━━━━━━━━━━\n\n"
    TEXT += f"» **Owner :** [𝙺𝙰𝙶𝚄𝚃𝚂𝚄𝙲𝙷𝙸](https://t.me/{OWNER_USERNAME})** \n\n"
    TEXT += f"» **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{telever}` \n\n"
    TEXT += f"» **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tlhver}` \n\n"
    TEXT += f"» **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pyrover}` \n━━━━━━━━━━━━━━━━━\n\n"
    BUTTON = [
        [
            Button.url("ʜᴇʟᴘ​", f"https://t.me/{dispatcher.bot.username}?start=help"),
            Button.url("sᴜᴘᴘᴏʀᴛ​", f"https://t.me/{SUPPORT_CHAT}"),
        ]
    ]
    ran = random.choice(PHOTO)
    await tbot.send_file(event.chat_id, ran, caption=TEXT, buttons=BUTTON)
