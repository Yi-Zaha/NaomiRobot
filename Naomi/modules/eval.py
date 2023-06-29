import io
import os
import textwrap
import traceback
from contextlib import redirect_stdout

from Naomi import LOGGER, dispatcher
from Naomi.modules.helper_funcs.chat_status import dev_plus
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler, run_async

namespaces = {}


def namespace_of(chat, update, bot):
    if chat not in namespaces:
        namespaces[chat] = {
            "__builtins__": globals()["__builtins__"],
            "bot": bot,
            "effective_message": update.effective_message,
            "effective_user": update.effective_user,
            "effective_chat": update.effective_chat,
            "update": update,
        }

    return namespaces[chat]


def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info(f"IN: {update.effective_message.text} (user={user}, chat={chat})")


def send(msg, bot, update):
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


@dev_plus
@run_async
def evaluate(update: Update, context: CallbackContext):
  try:
        cmd = event.text.markdown.split(" ", maxsplit=1)[1]
    except IndexError:
        return await event.reply("`Give something to execute...`")
    e = await event.reply("`Processing ...`")
    reply_to_id = event.reply_to_message_id or event.id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**✦ Code :**\n`{}` \n\n **✦ Result :** \n`{}` \n".format(
        cmd, evaluation
    )
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(evaluation)) as out_file:
            out_file.name = "eval.txt"
            await app.send_document(
                event.chat.id,
                out_file,
                force_document=True,
                caption=f"`{cmd}`" if len(cmd) < 998 else None,
                parse_mode=ParseMode.MARKDOWN,
                reply_to_message_id=reply_to_id,
            )
            await e.delete()
    else:
        await e.edit(
            final_output, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )



@dev_plus
@run_async
def execute(update: Update, context: CallbackContext):
    bot = context.bot
    send(do(exec, bot, update), bot, update)


def cleanup_code(code):
    if code.startswith("```") and code.endswith("```"):
        return "\n".join(code.split("\n")[1:-1])
    return code.strip("` \n")


def do(func, bot, update):
    log_input(update)
    content = update.message.text.split(" ", 1)[-1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, bot)

    os.chdir(os.getcwd())
    with open(
        os.path.join(os.getcwd(), "Naomi/modules/helper_funcs/temp.txt"), "w",
    ) as temp:
        temp.write(body)

    stdout = io.StringIO()

    to_compile = (
        f"def func(): "
        + "".join(f"\n {l}" for l in body.split("\n"))
    )

    try:
        exec(to_compile, env)
    except Exception as e:
        return f"{e.__class__.__name__}: {e}"

    func = env["func"]

    try:
        with redirect_stdout(stdout):
            func_return = func()
    except Exception as e:
        value = stdout.getvalue()
        return f"{value}{traceback.format_exc()}"
    else:
        value = stdout.getvalue()
        result = None
        if func_return is None:
            if value:
                result = f"{value}"
            else:
                try:
                    result = f"{repr(eval(body, env))}"
                except:
                    pass
        else:
            result = f"{value}{func_return}"
        if result:
            return result


@dev_plus
@run_async
def clear(update: Update, context: CallbackContext):
    bot = context.bot
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)


EVAL_HANDLER = CommandHandler(("e", "ev", "eva", "eval"), evaluate)
EXEC_HANDLER = CommandHandler(("x", "ex", "exe", "exec", "py"), execute)
CLEAR_HANDLER = CommandHandler("clearlocals", clear)

dispatcher.add_handler(EVAL_HANDLER)
dispatcher.add_handler(EXEC_HANDLER)
dispatcher.add_handler(CLEAR_HANDLER)

__mod_name__ = "Eval Module"
