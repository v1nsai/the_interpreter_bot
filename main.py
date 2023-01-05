import logging
import telegram
import os
import html
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import translate_v2 as translate

# Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
target_language = ''

# Make the bot talk to just me and my friends, the Google Translate API is unfortunately not free
allowed_ids = open('allowed_ids').read().splitlines()
allowed_ids = [int(i) for i in allowed_ids]

# Get API tokens
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="google_key.json"
bot_token = open('bot_token', 'r').read().rstrip('\n')

# Instantiate clients for Google Translate and Telegram
client = translate.Client()
bot = telegram.Bot(token=bot_token)
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Reads all messages sent to it, determines the language and translates to or from target_language
def auto_translate(update, context):
    if update.message.chat_id not in allowed_ids:
        context.bot.send_message(chat_id=update.message.chat_id, text="Sorry I'm not allowed to talk to strangers.  Send a message to @doctor_ew to learn more about me")
        return
    global target_language
    if target_language == '':
        context.bot.send_message(chat_id=update.message.chat_id, text='Set language with /set_target_language <2 letter language code>')
        return
    l = client.detect_language(update.message.text)
    language = l['language']
    if language == 'en':
        trans = client.translate(update.message.text, target_language=target_language)
    if language == target_language:
        trans = client.translate(update.message.text, target_language='en')
    context.bot.send_message(chat_id=update.message.chat_id, text=html.unescape(trans['translatedText']))

# Set the language to translate to and from
def set_target_language(update, context):
    if update.message.chat_id not in allowed_ids:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry I'm not allowed to talk to strangers.  Send a message to @doctor_ew to learn more about me")
        return
    global target_language
    if len(context.args) < 1 or len(context.args) > 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Set language with /set_target_language <2 letter language code>')
        return
    target_language = context.args[0]
    bot.send_message(chat_id=update.message.chat_id, text='Target language set to ' + target_language)

# Create handlers and add them to the dispatcher
dispatcher.add_handler(CommandHandler("set_target_language", set_target_language))
dispatcher.add_handler(MessageHandler(Filters.text, auto_translate))

# Starts listening for messages until the script is stopped
updater.start_polling()
updater.idle()
print('Interpreter is listening...')
