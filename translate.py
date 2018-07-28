# Imports the Google Cloud client library
from google.cloud import translate
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/doctor_ew/the-interpreter-bot-d5dad33f5ff8.json"

# Instantiates a client
client = translate.Client()

# The text to translate
text = u'Hello, world!'
# The target language
target = 'ru'

# Translates some text into Russian
translation = client.translate(
    text,
    target_language=target)

print(u'Text: {}'.format(text))
print(u'Translation: {}'.format(translation['translatedText']))