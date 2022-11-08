from telegram.utils import helpers
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def welcome(update, context):
    if not update.message.new_chat_members[0].is_bot:
        bot = context.bot
        url = helpers.create_deep_linked_url(context.bot.get_me().username, 'city-cs')
        text = "歡迎嚟到City CS討論區！\n可以用bot睇下新手攻略先\n有問題可以再問！"
        keyboard = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text='按下開啟bot', url=url)
        )
        for member in update.message.new_chat_members:
            update.message.reply_text(text, reply_markup=keyboard)
            new_members = update.message.new_chat_members
            firstname = member.first_name
            lastname = member.last_name
            if ("+852" in firstname):
                bot.kick_chat_member(chat_id=update.message.chat.id, user_id=update.message.from_user.id)
                return
            elif ("+852" in lastname):
                bot.kick_chat_member(chat_id=update.message.chat.id, user_id=update.message.from_user.id)
                return