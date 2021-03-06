# The Interpreter: A Telegram Bot

Huge credit and thanks goes out to everyone at [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for
making a Telegram bot wrapper that I could not refuse.  

Set up a virtual env 

`python3 -m venv pipenv`

Activate it 

`source pipenv/bin/activate`

Install packages 

`python3 -m pip install --upgrade python-telegram-bot google-cloud-translate`

In order to get this working you'll need to create your own Telegram bot (I'd share mine but the Google Translate API isn't free) by following the [instructions here](https://core.telegram.org/bots#6-botfather) then put your API key in a txt file and edit the line that defines `bot_token` in the `main.py` file.  Next you'll need to set up the Google Translate API, the starting point [can be found here.](https://cloud.google.com/translate/), then point the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the JSON file containing your key.

You'll also need to set the `bot_token` var to your bot's API token from Telegram, and set `allowed_ids` or comment out the var.

If you want it to be able to translate everything said in the group, you'll need change `/setprivacy` to `Disable` by telling @BotFather
