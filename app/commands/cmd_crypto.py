import json
import pickle
import requests

from math import log10, floor
from pycoingecko import CoinGeckoAPI

def round_sig(x, sig=2):
    return round(x, sig - int(floor(log10(abs(x)))) - 1)

def check_precision(p):
    start_count = False
    count = 0
    for idx in str(p):
        if start_count:
            count += 1
        elif idx == '.':
            start_count = True
    return str(count)

def price_string(p):
    p = p if p >= 100 else round_sig(p, 3)
    return ('${:,.' + check_precision(p) + 'f}').format(p)

def crypto(update, context):
    additional_coins = [{'id': 'avalanche-2', 'symbol': 'avax', 'name': 'Avalanche'}]
    if not context.args:
        update.message.reply_text("Symbol is missing, e.g. /crypto btc")
    elif len(context.args) > 1:
        update.message.reply_text("Only 1 symbol is required, e.g. /crypto btc")
    else:
        cg = CoinGeckoAPI()
        crypto_list = cg.get_coins_list()
        crypto_list.extend(additional_coins)
        text = ''
        for crypto in crypto_list:
            if crypto['symbol'] == context.args[0].lower():
                target_usd = cg.get_coins_markets(ids=crypto['id'], vs_currency='usd', price_change_percentage='1h,24h,7d')[0]
                if target_usd['market_cap_rank'] is None:
                    continue
                coingecko_url = 'https://www.coingecko.com/en/coins/' + crypto['id']
                twitter_url = 'https://twitter.com/search?q=%24' + crypto['symbol'].upper()
                target_hkd = cg.get_coins_markets(ids=crypto['id'], vs_currency='hkd', price_change_percentage='1h,24h,7d')[0]
                text += '<a href="{}">{}</a> - <a href="{}">${}</a> [{}]\n'.format(coingecko_url, target_usd['name'], twitter_url, target_usd['symbol'].upper(), target_usd['market_cap_rank'])
                text += '💰 Price [USD]: {}\n'.format(price_string(target_usd['current_price']))
                text += '⚖ H: {} | L: {}\n'.format(price_string(target_usd['high_24h']), price_string(target_usd['low_24h']))
                text += '🇭🇰 Price [HKD]: {}\n'.format(price_string(target_hkd['current_price']))
                text += '📈 ' if target_usd['price_change_percentage_1h_in_currency'] > 0 else '📉 '
                text += '1h: {:,.2f}%\n'.format(target_usd['price_change_percentage_1h_in_currency'])
                text += '📈 ' if target_usd['price_change_percentage_24h_in_currency'] > 0 else '📉 '
                text += '24h: {:,.2f}%\n'.format(target_usd['price_change_percentage_24h_in_currency'])
                text += '📈 ' if target_usd['price_change_percentage_7d_in_currency'] > 0 else '📉 '
                text += '7d: {:,.2f}%\n'.format(target_usd['price_change_percentage_7d_in_currency'])
                text += '📊 Volume: ${:,.0f}\n'.format(target_usd['total_volume'])
                text += '💎 MarketCap: ${:,.0f}\n'.format(target_usd['market_cap'])
                break

        if text == '':
            update.message.reply_text("Couldn't find your Shitcoin!")

        else:
            # with open('pickles/crypto_dict.pickle', 'rb') as f:
            #     crypto_dict = pickle.load(f)
            # if context.args[0].upper() in crypto_dict:
            #     url = 'https://www.coingecko.com/coins/{}/sparkline'.format(crypto_dict[context.args[0].upper()])
            #     context.bot.send_message(chat_id=update.message.chat.id, text=text, parse_mode='HTML')
            #     return
            context.bot.send_message(chat_id=update.message.chat.id, text=text, parse_mode='HTML')
