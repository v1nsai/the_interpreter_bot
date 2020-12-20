import logging
import telegram
import os
import html
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import translate_v2 as translate

# Setup evil evil global vars
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
target_language = ''

# Make the bot talk to just me and my friends, sorry I'd share if Google were free!
allowed_ids = open('allowed_ids.txt').read().splitlines()
allowed_ids = [int(i) for i in allowed_ids]

# Set API tokens, I had issues with setting the var in ~/.profile
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="the-interpreter-bot-d5dad33f5ff8.json"
bot_token = open('the-interpreter-bot-api-key.txt', 'r').read().rstrip('\n')

# Instantiates clients for Google Translate and Telegram
client = translate.Client()
bot = telegram.Bot(token=bot_token)
updater = Updater(token=bot_token)
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
def set_target_language(bot, update, args):
    if update.message.chat_id not in allowed_ids:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry I'm not allowed to talk to strangers.  Send a message to @doctor_ew to learn more about me")
        return
    global target_language
    if len(args) < 1 or len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Set language with /set_target_language <2 letter language code>')
        return
    target_language = args[0]
    bot.send_message(chat_id=update.message.chat_id, text='Target language set to ' + target_language)

# Create handlers and add them to the dispatcher
auto_translate_handler = MessageHandler(Filters.text, auto_translate)
set_target_language_handler = CommandHandler('set_target_language', set_target_language, pass_args=True)

dispatcher.add_handler(auto_translate_handler)
dispatcher.add_handler(set_target_language_handler)

# Starts listening for messages until the script is stopped
updater.start_polling()
updater.idle()
