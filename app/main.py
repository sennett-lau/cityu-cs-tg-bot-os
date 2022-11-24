import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler

from commands.hub import *
from conversations.hub import *
from message_handlers.hub import *
from modules.hub import *

load_dotenv()

APP_ENV = os.getenv('APP_ENV') # prd / dev
TOKEN = os.environ.get("TOKEN")
PORT = int(os.environ.get("PORT", "8443"))

def main():
    print('=======================================================')
    if APP_ENV != 'prd':
        print('Testing Environment...')
    else:
        print('Product Environment...')
    print('=======================================================')
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True, workers=6)

    dp = updater.dispatcher

    # Command handler
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("launchbot", launchbot))
    dp.add_handler(CommandHandler("updatelog", updatelog))
    dp.add_handler(CommandHandler('geguide', geguide))
    dp.add_handler(CommandHandler('wantpokemon', wantpokemon))
    dp.add_handler(CommandHandler('my903', my903))
    dp.add_handler(CommandHandler('crypto', crypto))
    dp.add_handler(CommandHandler('worldcup', worldcup))

    dp.add_handler(CommandHandler("start", start, filters=~Filters.group))
    dp.add_handler(CommandHandler('pin', pin, filters=~Filters.group))

    # Message handler
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, remove_member))

    # Conversation handler
    dp.add_handler(source_conv_handler)

    # Error handler
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

'''
help - show all command
launchbot - launch the bot and get some help
updatelog - get update log
geguide - get quick link to ge guide
wantpokemon - send you a pokemon!
my903 - check out this week's top 10 songs
crypto - check crypto price
'''