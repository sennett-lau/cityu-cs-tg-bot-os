import sys
import re

from datetime import datetime, timedelta

sys.path.append('../modules')
from modules.hub import *

matchStatus = {
    'finished': 'Finished',
    'h1': 'In Progress',
    'h2': 'In Progress',
    'notstarted': 'Not Started',
}

groupLetter = re.compile('^[a-hA-H]$').search

def worldcup(update, context):
    if not context.args or context.args[0] == 'help':
        worldcup_help(update, context)
    elif context.args[0] == 'tdy':
        jwt = wc_api_login()
        worldcup_tdy(update, context, jwt)
    elif context.args[0] == 'ytd':
        jwt = wc_api_login()
        worldcup_ytd(update, context, jwt)
    elif context.args[0] == 'tmr':
        jwt = wc_api_login()
        worldcup_tmr(update, context, jwt)
    elif context.args[0] == 'standings':
        jwt = wc_api_login()
        worldcup_standing(update, context, jwt, context.args[1])
    else:
        worldcup_error(update, context)
def worldcup_help(update, context):
    text = '⚽World Cup 2022 Functions are now LIVE!🏆\n\n'
    text += '/worldcup tdy - Get today\'s matches\n'
    text += '/worldcup ytd - Get yesterday\'s matches\n'
    text += '/worldcup tmr - Get tomorrow\'s matches\n'
    text += '/worldcup standings [Group] - Get current standings, Group A to H (e.g. /worldcup standings H)'
    update.message.reply_text(text)

def worldcup_error(update, context):
    update.message.reply_text("Unknown command")

def worldcup_tdy(update, context, jwt):
    reply = 'Today\'s matches:\n\n'

    today = datetime.now().strftime('%m/%d/%Y')

    reply = worldcup_get_match_by_date(jwt, reply, today)

    update.message.reply_text(reply)

def worldcup_ytd(update, context, jwt):
    reply = 'Yesterday\'s matches:\n\n'

    ytd = datetime.now()
    ytd = ytd - timedelta(hours=24)
    ytd = ytd.strftime('%m/%d/%Y')

    reply = worldcup_get_match_by_date(jwt, reply, ytd)

    update.message.reply_text(reply)

def worldcup_tmr(update, context, jwt):
    reply = 'Tomorrow\'s matches:\n\n'

    tmr = datetime.now()
    tmr = tmr + timedelta(hours=24)
    tmr = tmr.strftime('%m/%d/%Y')


    reply = worldcup_get_match_by_date(jwt, reply, tmr)

    update.message.reply_text(reply)

def worldcup_get_match_by_date(jwt, reply, date):
    matches = wc_api_get_match_by_date(jwt, date)

    for match in matches:
        time = datetime.strptime(match['local_date'], '%m/%d/%Y %H:%M')
        time = time + timedelta(hours=5)
        time = time.strftime('%m/%d/%Y %H:%M')
        reply += get_flag(match['home_team_en']) + ' ' + time + ' ' + get_flag(match['away_team_en']) + '\n'
        reply += match['home_team_en']
        reply += ' vs '
        reply += match['away_team_en'] + '\n'
        reply += str(match['home_score']) + ' : ' + str(match['away_score']) + ' (' + matchStatus[
            match['time_elapsed']] + ')' + '\n\n'

    return reply

def worldcup_standing(update, context, jwt, letter):
    reply = 'Current standings:\n\n'
    letter = letter.upper()
    a = bool(groupLetter(letter))
    if not bool(groupLetter(letter)):
        update.message.reply_text('Invalid Input, Please input /worldcup standings [Group]. Group A to H')

    groupStandings = wc_api_get_standings(jwt, letter)

    reply += 'Group: ' + letter + '\n\n'
    teams = groupStandings[0]['teams']
    for team in teams:
        reply += get_flag(team['name_en']) + team['name_en'] + '\n'
        reply += 'Matches played: ' + team['mp'] + '\n'
        reply += 'Matches won: ' + team['w'] + '\n'
        reply += 'Matches lost: ' + team['l'] + '\n'
        reply += 'Score: ' + team['pts'] + '\n'
        reply += 'Goals for: ' + team['gf'] + '\n'
        reply += 'Goals against: ' + team['ga'] + '\n'
        reply += 'Goals difference: ' + team['gd'] + '\n'
        reply += 'Drawn: ' + team['d'] + '\n'
        reply += '\n'
    reply += '\n\n'

    update.message.reply_text(reply)


