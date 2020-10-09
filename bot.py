from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import re, time, os

import classes.Student_In_Meeting as sim

DEBUG = False
TOKEN = str(os.environ['TOKEN'])
ADMIN = ['460390112']
student = None


def start(update, context):
    print("start")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Привіт. Я можу під'єднатись під будь яким іменем "+
                             "до конференції на сайті https://bbb.comsys.kpi.ua/\n"+
                             "Просто відправ мені посилання у першому рядку та нік у другому.")


def end(update, context):
    global student
    print('end')
    if student is not None:
        student.exit_meeting()


def go_in(update, context):
    global student
    input_data = update.message.text.split('\n')
    print(start, input_data)
    student = sim.Student_In_Meeting()
    is_connected = student.go_in_meeting(*input_data)
    if not is_connected:
        context.bot.send_message(chat_id=ADMIN[0],
                             text="ERROR!\n"+str(input_data))
        context.bot.send_message(chat_id=update.effective_chat.id,
                             text="На даний момент неможливо підключитись до даної конференції. Спробуйте пізніше.")
        student.browse_quit()
    

def echo(update, context):
    print(update.message.text, '\n', update.effective_chat.id)    


updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('end', end))

dispatcher.add_handler(MessageHandler(Filters.regex('^(https?:\/\/(www\.)?bbb\.comsys\.kpi\.ua\/b\/[\w\-]+)\n([\w\s-]+)$'), go_in))

if DEBUG:
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()
else:
    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get('PORT', '8443')),
                          url_path=TOKEN)
    updater.bot.set_webhook("https://testbot2202.herokuapp.com/" + TOKEN)

updater.idle()
