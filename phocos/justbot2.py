from telegram import Bot
from phocos import get_latest_status
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json

TOKEN = "TELEGRAM_TOKEN"

def echo(update, context):
    text = update.message.text
    print(update.effective_chat.id)
    if text == "status":
        current_status = get_latest_status()
        m = f"""Latest phocos info

    ```
    {current_status}
    ```"""
        context.bot.send_message(update.effective_chat.id, m, parse_mode="markdown")


def main():
    bot = Bot(TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()

if __name__ == '__main__':
    main()
