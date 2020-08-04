from telegram.ext import Updater
updater = Updater(token='1176844516:AAFzHPuP3kYv6VGbJI6mt7GTnMXgj-Qknwo', use_context=True)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please send /get command if you want see you rating.")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

import vgu_ratings
def get(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text=vgu_ratings.get_rating_doc())

dispatcher.add_handler(CommandHandler('get', get))

updater.start_polling()
