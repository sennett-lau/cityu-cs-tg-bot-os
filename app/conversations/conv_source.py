import requests
import sys

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Filters, CallbackQueryHandler, ConversationHandler

sys.path.append('../modules')
from modules.hub import *

Subject, Type, File = range(3)

file_subject = ''
file_type = ''

def source(update, context):
    keyboard = [
        [InlineKeyboardButton("CS3334 Data Structure", callback_data='CS3334 Data Structure')],
        [InlineKeyboardButton("CS3481 Fundamentals of Data Science",
                              callback_data='CS3481 Fundamentals of Data Science')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Select a subject:'

    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=reply_markup, text=text)

    return Subject


def source_subject_query(update, context):
    query = update.callback_query
    query.answer()

    global file_subject
    file_subject = query.data

    if query.data == 'CS3334 Data Structure':
        keyboard = [
            [InlineKeyboardButton("Weekly Coding", callback_data='Weekly Coding')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = 'Select a source type'

        query.edit_message_text(reply_markup=reply_markup, text=text)
    elif query.data == 'CS3481 Fundamentals of Data Science':
        keyboard = [
            [InlineKeyboardButton("Lecture Notes", callback_data='Lecture Notes')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = 'Select a source type'

        query.edit_message_text(reply_markup=reply_markup, text=text)

    return Type


def source_type_query(update, context):
    query = update.callback_query
    query.answer()

    global file_type
    file_type = query.data

    keyboard = []
    if query.data == 'Weekly Coding':
        qno = [
            '78',
            '142',
            '185',
            '272',
            '372',
            '438',
            '737', '738', '739',
            '740', '741', '742', '743', '744', '745', '746', '747', '748', '749',
            '750', '751', '752', '753', '754', '755', '756', '757', '758',
            '767',
            '814', '819',
            '820', '823', '825', '827', '828',
            '831', '832', '836'
        ]
        for no in qno:
            keyboard += [[InlineKeyboardButton(no, callback_data=no + '.cpp')]]
    elif query.data == 'Lecture Notes':
        files = ['all', '1_Introduction', '2_Data', '3_Decision Tree',
                 '4_Classifier Evaluation', '5_Nearest Neighbor Classifier Probabilistic Classification',
                 '6_Cluster Analysis (Kmeans)', '7_Cluster Analysis (Hierarchical Clustering)',
                 '8_Association Analysis']
        for file in files:
            file_format = '.zip' if file == 'all' else '.pdf'
            keyboard += [[InlineKeyboardButton(file, callback_data=file + file_format)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = 'Please select'

    query.edit_message_text(reply_markup=reply_markup, text=text)

    return File


def file_handler(update, context):
    query = update.callback_query
    update.callback_query.answer()

    global file_subject
    global file_type

    path = "https://github.com/laub1199/cityu-cs-tg-bot/raw/master/source/"
    document = path + '{}/{}/'.format(file_subject, file_type) + str(query.data)

    if '.cpp' in query.data:
        document = requests.get(document).content

    query.edit_message_text(text="Selected option: {}".format(query.data))

    context.bot.sendDocument(chat_id=query.message.chat.id, document=document, filename=query.data)
    print('{} - {} requested for {}/{}/{}'.format(query.message.chat.username, query.message.chat.first_name,
                                                  file_subject, file_type, query.data))
    return ConversationHandler.END


source_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('source', source, filters=~Filters.group)],
    states={
        Subject: [CallbackQueryHandler(source_subject_query)],
        Type: [CallbackQueryHandler(source_type_query)],
        File: [CallbackQueryHandler(file_handler)]
    },
    fallbacks=[CommandHandler('end', end)],
)