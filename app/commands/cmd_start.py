def start(update, context):
    chat_id = update.message.chat.id
    text = open("txts/start.txt", "r", encoding="utf-8").read()
    context.bot.sendMessage(chat_id=chat_id, text=text, parse_mode='HTML')
