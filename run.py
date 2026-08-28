import os
import subprocess

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from wakeonlan import send_magic_packet


IDs = set((int(idn) for idn in os.environ["VALID_IDS"].split("|")))

print(IDs)
print(os.environ["VALID_IDS"])


COMPUTERS = {}
for entry in os.environ["COMPUTERS"].split("|"):
    name, mac = entry.split("-")
    COMPUTERS[name] = entry


async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in IDs:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Who are you?? Get lost"
        )
        return

    if len(context.args) < 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"wake what? your choices: {', '.join(COMPUTERS.keys())}",
        )
        return

    if len(context.args) > 1:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="too many arguments, send only one"
        )
        return

    if context.args[0] not in COMPUTERS:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"unknown computer, your choices: {', '.join(COMPUTERS.keys())}",
        )
        return

    send_magic_packet(COMPUTERS[context.args[0]])

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Your computer is waking up"
    )


async def send_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in IDs:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Who are you?? Get lost"
        )

    help_message = "Wake up a computer with /wake <name of your computer>"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)


if __name__ == "__main__":
    token = os.environ["TOKEN"]
    application = ApplicationBuilder().token(token).build()

    wake_pc = CommandHandler("wake", wake)
    help_handler = CommandHandler("help", send_help)

    application.add_handler(wake_pc)
    application.run_polling()
