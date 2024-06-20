import logging
import telegram
import os
import html
from telegram.ext import language, CommandHandler, MessageHandler, Filters
from google.cloud import translate_v2 as translate

# Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
target_language = ''

print("Loading required config files...")
if os.path.exists('/app/allowed_ids'):
    allowed_ids = open('/app/allowed_ids').read().splitlines()
    allowed_ids = [int(i) for i in allowed_ids]
else:
    print("No allowed_ids file found.  Please create a file in the project root called allowed_ids with a list of group chat IDs (one per line) that the bot is allowed to interact with.  Find your group chat ID by adding @getidsbot to the group you want to add.")
if os.path.exists('/app/google_key.json'):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/google_key.json"
else:
    print("No google_key.json file found.  Please create a service account and key for the Google Cloud Translation API and save it as google_key.json in the project root.  Instructions here https://cloud.google.com/translate/docs/setup")
if os.path.exists('/app/bot_token'):
    bot_token = open('/app/bot_token').read().rstrip('\n')
else:
    print("No bot_token file found.  Please create a file in the project root called bot_token and paste your Telegram bot token in there.  Instructions for getting a token here https://core.telegram.org/bots#6-botfather")

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
        context.bot.send_message(chat_id=update.message.chat_id, text='Set language with /language <2 letter language code>')
        return
    l = client.detect_language(update.message.text)
    language = l['language']
    if language == 'en':
        trans = client.translate(update.message.text, target_language=target_language)
    if language == target_language:
        trans = client.translate(update.message.text, target_language='en')
    context.bot.send_message(chat_id=update.message.chat_id, text=html.unescape(trans['translatedText']))

# Set the language to translate to and from    
def language(update, context):
    if update.message.chat_id not in allowed_ids:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry I'm not allowed to talk to strangers.  Send a message to @doctor_ew to learn more about me")
        return
    global target_language
    if len(context.args) < 1 or len(context.args) > 1:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Set language with /language <2 letter ISO 639 language code>')
        return
    target_language = context.args[0]
    bot.send_message(chat_id=update.message.chat_id, text='Target language set to ' + target_language)

# Create handlers and add them to the dispatcher
dispatcher.add_handler(CommandHandler("language", language))
dispatcher.add_handler(MessageHandler(Filters.text, auto_translate))

# Starts listening for messages until the script is stopped
updater.start_polling()
updater.idle()
print('Interpreter is listening...')
