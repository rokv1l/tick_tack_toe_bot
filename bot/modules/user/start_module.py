
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from config import user_messages


async def start_callback(update: Update, context: CallbackContext) -> None:
    await update.effective_chat.send_message(user_messages["start_callback_0"])


start_handler = CommandHandler("start", start_callback)
