from os import remove

from pyrogram import filters
from pyrogram.types import ChatPermissions, ChatMember
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    run_async,
)
from Naomi.utils.permissions import adminsOnly
from Naomi.modules.disable import DisableAbleCommandHandler
from Naomi import BOT_USERNAME as bn, BOT_ID, dispatcher
from Naomi import pbot, arq
from Naomi.utils.errors import capture_err
from Naomi.utils.filter_groups import nsfw_detect_group

__mod_name__ = "Anti-NSFW​"


async def get_file_id_from_message(message):
    file_id = None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type != "image/png" and mime_type != "image/jpeg":
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


@pbot.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=nsfw_detect_group,
)
@run_async
@pbot.on_message(filters.command("antinsfw"))
async def antinsfw(_, message):
    if not message.from_user:
        return
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return
    file = await pbot.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    if not results.ok:
        return
    results = results.result
    remove(file)
    nsfw = results.is_nsfw
    if not nsfw:
        return
    try:
        await message.delete()
    except Exception:
        return
    await message.reply_text(
        f"""
**NSFW Image Detected & Deleted Successfully!
————————————————————**
**User:** {message.from_user.mention} [`{message.from_user.id}`]
**Safe:** `{results.neutral} %`
**Porn:** `{results.porn} %`
**Adult:** `{results.sexy} %`
**Hentai:** `{results.hentai} %`
**Drawings:** `{results.drawings} %`
**————————————————————**
__Use `/disable antinsfw` to disable this.__
"""
    )

@run_async
@pbot.on_message(filters.command("nsfwscan"))
@capture_err
async def nsfwscan(_, message):
    if not message.reply_to_message:
        await message.reply_text(
            "`Reply to an image/document/sticker/animation to scan it.`"
        )
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    m = await message.reply_text("`Scanning...`")
    file_id = await get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("`Something wrong happened...|")
    file = await pbot.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
**Neutral:** `{results.neutral} %`
**Porn:** `{results.porn} %`
**Hentai:** `{results.hentai} %`
**Sexy:** `{results.sexy} %`
**Drawings:** `{results.drawings} %`
**NSFW:** `{results.is_nsfw}`
"""
    )


ANTINSFW_HANDLER = DisableAbleCommandHandler("antinsfw", antinsfw)
NSFWSCAN_HANDLER = DisableAbleCommandHandler("nsfwscan", nsfwscan)

dispatcher.add_handler(ANTINSFW_HANDLER)
dispatcher.add_handler(NSFWSCAN_HANDLER)

__command_list__ = [
    "antinsfw", "nsfwscan"]

__mod_name__ = "Antinsfw"

__handlers__ = [
    ANTINSFW_HANDLER,
    NSFWSCAN_HANDLER,]
