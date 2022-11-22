import sys
import datetime

sys.path.append('../modules')
from modules.hub import *

matchStatus = {
    'finished': 'Finished',
    'h1': 'In Progress',
    'h2': 'In Progress',
    'notstarted': 'Not Started',
}

def worldcup(update, context):
    jwt = wc_api_login()
    if not context.args:
        update.message.reply_text("Please enter a country name")
    elif context.args[0] == 'today':
        reply = 'Today\'s matches:\n\n'

        today = datetime.datetime.now().strftime('%m/%d/%Y')

        matches = wc_api_get_match_by_date(jwt, today)

        for match in matches:
            reply += match['local_date'] + '\n'
            reply += get_flag(match['home_team_en']) + ' vs ' + get_flag(match['away_team_en']) + '\n'
            reply += str(match['home_score']) + ' : ' + str(match['away_score']) + ' (' + matchStatus[match['time_elapsed']] + ')' + '\n\n'

        update.message.reply_text(reply)
    else:
        update.message.reply_text("Unknown command")