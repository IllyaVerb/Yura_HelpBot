from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import re, time, os

import classes.Student_In_Meeting as sim

DEBUG = False
TOKEN = os.environ['TOKEN']
ADMIN = '460390112'

""" Not in development
SCHEDULE = {
	1: ((8, 30), (10, 5)),
	2: ((10, 25), (12, 0)),
	3: ((12, 20), (13, 55)),
	4: ((14, 15), (15, 50)),
	5: ((16, 10), (17, 45))
}
"""
# DB format = CHAT_ID: {'tab_handler':None, 'input_data':None, 'message_mode':False}
DATABASE = {}

""" Not in development
def current_lec_ending(time_struct):
	hour = time_struct.tm_hour
	minute = time_struct.tm_min
	week = time_struct.tm_wday
	
	lec_ending = list(time_struct)
	for i, j in SCHEDULE.items():
		if j[1][0] <= hour and j[1][1] <= minute and week != 6:
			lec_ending[3] = hour
			lec_ending[4] = minute

	return time.mktime(tuple(lec_ending))
"""

# Start working with bot
def start(update, context):
	print('Enetered command <start>\n', DATABASE)
	context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(),
							 text="Привіт. Я можу під'єднатись під будь яким іменем "+
							 "до конференції на сайті https://bbb.comsys.kpi.ua/\n"+
							 "Просто відправ мені посилання у першому рядку та нік у другому.")


# Leaving conference
def end(update, context):
	user_id = update.effective_chat.id

	print('Enetered command <end>\n', DATABASE)
	try:
		if 	user_id in DATABASE and \
			DATABASE[user_id] is not None and \
			student.exit_meeting(DATABASE[user_id]['tab_handler']):

			DATABASE[user_id] = {'tab_handler': None, 'input_data': None, 'message_mode': False}
			context.bot.send_message(chat_id=user_idt.id,
									 text="Ви залишили конференцію. Було приємно співпрацювати, звертайтесь)")
		else:
			context.bot.send_message(chat_id=user_id,
								 	 text="Ви не можете залишити конференцію, бо зараз не знаходитесь у жодній.")
	
	except Exception as e:
		context.bot.send_message(chat_id=ADMIN,
								  text="ERROR!\n"+e)


# Not in development
def msg_mode(update, context):
	if update.effective_chat.id in DATABASE and DATABASE[update.effective_chat.id] is not None:
		DATABASE[update.effective_chat.id]['message_mode'] = not DATABASE[update.effective_chat.id]['message_mode']

		if DATABASE[update.effective_chat.id]['message_mode']:
			context.bot.send_message(chat_id=update.effective_chat.id,
									 text="Ви .")

	else:
		context.bot.send_message(chat_id=update.effective_chat.id,
								 text="Ви не можете працювати з повідомленнями, бо зараз не знаходитесь у конференції.")
# Not in development


# Participate in conference
def go_in(update, context):
	global student

	user_id = update.effective_chat.id
	
	# input_data is in format '[link on meeting, name for meeting]'
	input_data = update.message.text.split('\n')
	
	print('Enetered command <join>\n', input_data)
	# You are in any conference
	if user_id in DATABASE and \
		DATABASE[user_id]['tab_handler'] is not None:
		
		context.bot.send_message(chat_id=user_id,
								 text="Ви вже знаходитесь на лекції, для нового підключення вийдіть з минулого " +
									  "(команда /end), або дочекайтесь його закінчення.")
		return

	# Try to join
	connecting_answ = student.go_in_meeting(*input_data)

	# <false> if not active meeting
	is_connected = connecting_answ['status']
	if not is_connected:
		DATABASE[user_id] = {'tab_handler': None, 'input_data': None, 'message_mode': False}
		
		context.bot.send_message(chat_id=ADMIN,
								 text="ERROR!\n"+str(input_data))
		context.bot.send_message(chat_id=user_id,
								 text="На даний момент неможливо підключитись до даної конференції. Спробуйте пізніше.")
		student.remove_current_tab()
	else:
		DATABASE[user_id] = {'tab_handler': connecting_answ['tab_handler'],
											  'input_data': input_data,
											  'message_mode': False}
		context.bot.send_message(chat_id=user_id,
								 text="Ви успішно приєднались до конференції в режимі слухача, під ніком: " +
									  input_data[1])
		
	
def echo(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text) 

	
def unknown_cmd(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Я Вас не розумію (") 


updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('end', end))
# dispatcher.add_handler(CommandHandler('message_mode', msg_mode))

dispatcher.add_handler(MessageHandler(
	Filters.regex(r'^(https?:\/\/(www\.)?bbb\.comsys\.kpi\.ua\/b\/[\w\-]+)\n([\w\s-]+)$'), go_in))

dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), unknown_cmd))

if DEBUG:
	# dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
	updater.start_polling()
else:
	updater.start_webhook(listen="0.0.0.0",
						  port=int(os.environ.get('PORT', '8443')),
						  url_path=TOKEN)
	updater.bot.set_webhook("https://yurahelpbot.herokuapp.com/" + TOKEN)

# create new active student
student = sim.Student_In_Meeting()
#student.new_tab('https://www.google.com/')

updater.idle()
