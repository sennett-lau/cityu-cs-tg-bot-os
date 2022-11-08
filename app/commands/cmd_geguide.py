from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def geguide(update, context):
    if not context.args:
        update.message.reply_text("Course code missing, e.g. /geguide ge1401")
    elif len(context.args) > 1:
        update.message.reply_text("Only 1 course code is required, e.g. /geguide ge1401")
    else:
        url = 'http://cityuge.swiftzer.net/courses/' + str(context.args[0]).lower()
        text = 'Check out ' + str(context.args[0]).upper() + '!'
        keyboard = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(text=text, url=url)
        )

        update.message.reply_text("Quick link!", reply_markup=keyboard)
