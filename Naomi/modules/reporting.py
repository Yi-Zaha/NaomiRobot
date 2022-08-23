from pyrogram import filters
from pyrogram.types import  Message
from Naomi import pbot as app
from Naomi.mongo.reportdb import Reporting
from Naomi.utils.commands import command
from Naomi.utils.permissions import adminsOnly


@app.on_message(filters.command("reports") & ~filters.private))
@adminsOnly("can_change_info")
async def report_setting(_, m: Message):
    args = m.text.split()
    db = Reporting(m.chat.id)
    if m.chat.type == "private":
        if len(args) >= 2:
            option = args[1].lower()
            if option in ("yes", "on", "true"):
                db.set_settings(True)
                await m.reply_text("Turned on reporting! You'll be notified whenever anyone reports something in groups you are admin.")
            elif option in ("no", "off", "false"):
                db.set_settings(False)
                await m.reply_text("Turned off reporting! You wont get any reports.")
        else:
            await m.reply_text(f"Your current report preference is: `{(db.get_settings())}`\n\nTo change this setting, try this command again, with one of the \nfollowing args: yes/no/on/off")
    elif len(args) >= 2:
        option = args[1].lower()
        if option in ("yes", "on", "true"):
            db.set_settings(True)
            await m.reply_text("Turned on reporting! Admins who have turned on reports will be notified when /report or @admin is called.")
        elif option in ("no", "off", "false"):
            db.set_settings(False)
            await m.reply_text("Turned off reporting! No admins will be notified on /report or @admin.")
    else:
        await m.reply_text(
            f"""
Reports are currently `{(db.get_settings())}` in this chat.
Tochange this setting, try this command again, with one of the following args: `yes/no/on/off`"""
        )



  
@app.on_message(
    (
            filters.command("report")
            | filters.command(["admins", "admin"], prefixes="@")
    )
    & ~filters.private
)
async def report_user(_, message):
    db = Reporting(message.chat.id)
    if not db.get_settings():
        return
    text = f"Reported to admins!"
    admin_data = await app.get_chat_members(chat_id=message.chat.id, filter="administrators")
    for admin in admin_data:
        if admin.user.is_bot or admin.user.is_deleted:
            continue
        text += f"[\u2063](tg://user?id={admin.user.id})"
    await message.reply_to_message.reply_text(text)




__mod_name__ = "Reports"
__help__ = """
**User commands:**
- /report: Reply to a message to report it for admins to review.
- admin: Same as /report
**Admin commands:**
- /reports `<yes/no/on/off>`: Enable/disable user reports.
To report a user, simply reply to his message with @admin or /report;
