def updatelog(update, context):
    chat_id = update.message.chat.id
    with open("txts/update_log.txt") as myfile:
        text = ''.join(str(s) for s in [next(myfile) for x in range(8)])
    context.bot.sendMessage(chat_id=chat_id, text=text, parse_mode='HTML')
