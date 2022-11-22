import sys

sys.path.append('../modules')
from modules.hub import *

def worldcup(update, context):
    if not context.args:
        update.message.reply_text("Please enter a country name")
    else:
        country = context.args[0]
        flag = getFlags(country)

        update.message.reply_text(flag)