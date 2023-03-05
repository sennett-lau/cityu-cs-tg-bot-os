import sys

sys.path.append('../modules')
from modules.hub import *

P_BANDAI_URL = 'https://p-bandai.com/hk'

def pbandai(update, context):
	html = get_web_data(P_BANDAI_URL)
	
	if not context.args or context.args[0] == 'help':
		prompt_help(update, context)
		return
	elif context.args[0] == 'new':
		new_arrivals_products = get_new_arrivals(html)
		prompt_new_arrivals(update, context, new_arrivals_products)
	else:
		update.message.reply_text('Unknown command')

def get_new_arrivals(html):
	new_arrivals_section = html.find('section', {'class': 'o-grid--newarrival'})
	new_arrivals_raw = new_arrivals_section.find_all('a', {'class': 'm-card'})
	
	new_arrivals_products = []
	
	i = 0
	
	for item in new_arrivals_raw:
		product = {
			'img': item.find('img')['src'],
			'release_date': date_formatter(item.find('p', {'class': 'm-card__release'}).text),
			'name': item.find('p', {'class': 'm-card__name'}).text,
			'price': item.find('p', {'class': 'm-card__price'}).text,
			'link': 'https://p-bandai.com' + item['href'],
		}
		
		new_arrivals_products.append(product)
		
		i += 1
		if i >= 3:
			break
	
	return new_arrivals_products

def prompt_help(update, context):
	help_text = 'P-Bandai Command\n\n'
	help_text += '/pbandai help - 顯示此訊息\n'
	help_text += '/pbandai new - 顯示3件最新的上市商品'
	
	context.bot.send_message(chat_id=update.message.chat.id, text=help_text)

def prompt_new_arrivals(update, context, products):
	for product in products:
		photo_url = product['img']
		caption = product['name'] + '\n\n'
		caption += product['price'] + '\n\n'
		caption += '販售時間：' + product['release_date'] + '\n\n'
		caption += product['link']
		
		context.bot.send_photo(chat_id=update.message.chat.id, photo=photo_url, caption=caption)

def date_formatter(date):
	date = date.replace(' 發佈', '')
	formatted_date = date.split(' ')
	month = formatted_date[0].split('.')[0]
	day = formatted_date[0].split('.')[1]
	hour = formatted_date[1].split(':')[0]
	minute = formatted_date[1].split(':')[1]
	
	return month + '月' + day + '日 ' + hour + '時' + minute + '分'
