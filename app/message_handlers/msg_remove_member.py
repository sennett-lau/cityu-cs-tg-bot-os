def remove_member(update, context):
    context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)