import logging
import telegram
import os
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from google.cloud import translate

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set API tokens
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/path/to/key.json"
bot_token = open('/path/to/textfile/containing/api_key.txt', 'r').read().rstrip('\n')

# Instantiates clients for Google Translate and Telegram
client = translate.Client()
bot = telegram.Bot(token=bot_token)
updater = Updater(token=bot_token)
dispatcher = updater.dispatcher

target_language = ''

# Reads all messages sent to it, determines the language and translates to or from target_language
def auto_translate(bot, update):
    global target_language
    l = client.detect_language(update.message.text)
    language = l['language']
    if language == 'en':
        trans = client.translate(update.message.text, target_language=target_language)
    if language == target_language:
        trans = client.translate(update.message.text, target_language='en')
    bot.send_message(chat_id=update.message.chat_id, text=trans['translatedText'])

# Set the language to translate to and from
def set_target_language(bot, update, args):
    global target_language
    target_language = args[0]
    bot.send_message(chat_id=update.message.chat_id, text='Target language set to ' + target_language)

# Create handlers and add them to the dispatcher
auto_translate_handler = MessageHandler(Filters.text, auto_translate)
set_target_language_handler = CommandHandler('set_target_language', set_target_language, pass_args=True)
dispatcher.add_handler(auto_translate_handler)
dispatcher.add_handler(set_target_language_handler)

# Starts listening for messages until the script is stopped
updater.start_polling()
