import sys

from datetime import datetime, timedelta

sys.path.append('../modules')
from modules.hub import *

matchStatus = {
    'finished': 'Finished',
    'h1': 'In Progress',
    'h2': 'In Progress',
    'notstarted': 'Not Started',
}

def worldcup(update, context):
    if not context.args or context.args[0] == 'help':
        worldcup_help(update, context)
    elif context.args[0] == 'today':
        jwt = wc_api_login()
        worldcup_today(update, context, jwt)
    else:
        worldcup_error(update, context)
def worldcup_help(update, context):
    text = '⚽World Cup 2022 Functions are now LIVE!🏆\n\n'
    text += '/worldcup today - Get today\'s matches'
    update.message.reply_text(text)

def worldcup_error(update, context):
    update.message.reply_text("Unknown command")

def worldcup_today(update, context, jwt):
    reply = 'Today\'s matches:\n\n'

    today = datetime.now().strftime('%m/%d/%Y')

    matches = wc_api_get_match_by_date(jwt, today)

    for match in matches:
        time = datetime.strptime(match['local_date'], '%m/%d/%Y %H:%M')
        time = time + timedelta(hours=5)
        time = time.strftime('%m/%d/%Y %H:%M')
        reply += get_flag(match['home_team_en']) + ' ' + time + ' ' + get_flag(match['away_team_en']) + '\n'
        reply += match['home_team_en']
        reply += ' vs '
        reply += match['away_team_en'] + '\n'
        reply += str(match['home_score']) + ' : ' + str(match['away_score']) + ' (' + matchStatus[match['time_elapsed']] + ')' + '\n\n'

    update.message.reply_text(reply)