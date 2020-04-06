import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import TelegramError

# Enable logging 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Use your own API_TOKEN here
API_TOKEN = "TOKEN"

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    # Start monitoring messages and remove new user joined group message
    update.message.reply_text("Hello, I am the Thread Cleaner")

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('This bot automatically removes all user joined messages in a group if made admin')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def clean(update, context):
    try:
        context.bot.delete_message(update.message.chat.id, update.message.message_id)
    except TelegramError:
        pass

def main():
    updater = Updater(token=API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, clean))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
