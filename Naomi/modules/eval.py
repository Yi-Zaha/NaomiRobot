import io
import os
import sys
import textwrap
import traceback
from contextlib import redirect_stdout, suppress

from pyrogram import filters
from pyrogram.enums import ParseMode as PyroParseMode
from Naomi import DEV_USERS, LOGGER, dispatcher, pbot, TOKEN
from Naomi.modules.helper_funcs.chat_status import dev_plus
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, run_async

namespaces = {}

def namespace_of(chat, update, context):
    if chat not in namespaces:
        namespaces[chat] = {
            "__builtins__": globals()["__builtins__"],
            "update": update,
            "context": context,
        }

    return namespaces[chat]


def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info(f"IN: {update.effective_message.text} (user={user}, chat={chat})")


def send(msg, update, bot):
    if len(str(msg)) > 2000:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "output.txt"
            bot.send_document(chat_id=update.effective_chat.id, document=out_file)
    else:
        LOGGER.info(f"OUT: '{msg}'")
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"`{msg}`",
            parse_mode=ParseMode.MARKDOWN,
        )


@pbot.on_message(filters.command("eval") & filters.user(DEV_USERS))
async def eval_handler(client, message):
    if len(message.command) == 1:
        return await message.reply("Give something to evaluate.")

    cmd = message.text.markdown.split(" ", 1)[1]
    status_message = await message.reply("Processing...")

    old_stderr = sys.stderr
    old_stdout = sys.stdout

    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = exc if exc else (stderr if stderr else stdout)
    final_output = (
        f"**INPUT :**\n`{cmd}`\n\n**OUTPUT :**\n`{evaluation or 'Success'}`\n"
    )

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(evaluation)) as file:
            file.name = "eval.txt"
            await client.send_document(
                message.chat.id,
                file,
                caption=f"`{cmd[:998]}`",
                reply_to_message_id=message.reply_to_message_id or message.id,
                parse_mode=PyroParseMode.MARKDOWN,
            )
        await status_message.delete()
    else:
        await client.send_message(
            message.chat.id,
            final_output,
            reply_to_message_id=message.reply_to_message_id or message.id,
            parse_mode=PyroParseMode.MARKDOWN,
        )
        await status_message.delete()


async def aexec(code, message):
    exec(
        (
            "async def __aexec(client, message):\n"
            + "    p = print\n"
            + "    m = message\n"
            + "    reply = m.reply_to_message\n"
            + "    chat = m.chat.id"
        )
        + "".join(f"\n    {l}" for l in code.split("\n"))
    )

    return await locals()["__aexec"](message._client, message)


@dev_plus
def execute(update: Update, context: CallbackContext):
    bot = context.bot
    send(do(exec, update, context), update, bot)


def cleanup_code(code):
    if code.startswith("```") and code.endswith("```"):
        return "\n".join(code.split("\n")[1:-1])
    return code.strip("` \n")


def do(func, update, context):  # skipcq
    log_input(update)
    content = update.message.text.split(" ", 1)[-1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, context)

    os.chdir(os.getcwd())
    with open(
        os.path.join(os.getcwd(), "Naomi/modules/helper_funcs/temp.txt"),
        "w",
    ) as temp:
        temp.write(body)

    stdout = io.StringIO()

    to_compile = f'def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:  # skipcq PYL-W0703
        return f"{e.__class__.__name__}: {e}"

    func = env["func"]

    try:
        with redirect_stdout(stdout):
            func_return = func()
    except Exception:  # skipcq PYL-W0703
        value = stdout.getvalue()
        return f"{value}{traceback.format_exc()}"

    value = stdout.getvalue()
    result = None
    if func_return is None:
        if value:
            result = f"{value}"
        else:
            with suppress(Exception):
                result = f"{repr(eval(body, env))}"
    else:
        result = f"{value}{func_return}"

    if result:
        # don't send results if it has bot token inside.
        if TOKEN in result:
            result = "Results includes bot TOKEN, aborting..."
        return result


@dev_plus
def clear(update: Update, context: CallbackContext):
    bot = context.bot
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)

EXEC_HANDLER = CommandHandler(("x", "ex", "exe", "exec", "py"), execute)
CLEAR_HANDLER = CommandHandler("clearlocals", clear)

dispatcher.add_handler(EXEC_HANDLER)
dispatcher.add_handler(CLEAR_HANDLER)

__mod_name__ = "Eval Module"

