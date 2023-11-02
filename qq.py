from telegram.ext import ApplicationBuilder, MessageHandler, filters


async def all_callback(update, context):
    await update.effective_chat.send_message("Привет, я бот для будущей акции ROYAL RAVEN")


app = ApplicationBuilder().token("6635667361:AAFJfkq62epfyKsizRYS7QCMz7ZmlMbtS74").build()
app.add_handler(MessageHandler(filters.ALL, all_callback))
app.run_polling()
