import logging
from telegram import ParseMode,ChatAction
from telegram.ext import Updater, CommandHandler
from os import environ
import vgu_ratings

TOKEN = str(environ.get('TELEGRAM_BOT_TOKEN'))
PORT = int(environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
  """Simple /start command"""
  context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please send /get command if you want see you rating.")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def get(update, context):
  """Get ratings from database"""
  context.bot.send_message(chat_id=update.effective_chat.id, text=vgu_ratings.get_rating_doc())

def fetch(update, context):
  """Fetch ratings from VSU site"""
  context.bot.send_chat_action(chat_id=update.effective_chat.id, action = ChatAction.UPLOAD_DOCUMENT)

  updated = vgu_ratings.fetch_all_ratings()
  if updated:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ratings wil be *updated!*", parse_mode = ParseMode.MARKDOWN_V2)
  else:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Nothing changed.")

  context.bot.send_message(chat_id=update.effective_chat.id, text=vgu_ratings.get_rating_doc())

def main():
  updater = Updater(token=TOKEN, use_context=True)
  dispatcher = updater.dispatcher

  # Bot commands
  dispatcher.add_handler(CommandHandler('start', start))
  dispatcher.add_handler(CommandHandler('get', fetch))
  dispatcher.add_handler(CommandHandler('fetch', fetch))

  # Error handling
  dispatcher.add_error_handler(error)

  # We need use webhok instead start_pooling() because Heroku crash app
  # if we not listen in defined port
  updater.start_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=TOKEN)
  updater.bot.setWebhook('https://vsu-ratings.herokuapp.com/' + TOKEN)

  updater.idle()


if __name__ == '__main__':
    main()