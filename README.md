# The Interpreter: A Telegram Bot
<img src="https://github.com/v1nsai/the_interpreter_bot/assets/410443/205a8e6f-b361-4913-b500-fe7a81d9592b" width=256 height=256 />

Powered by [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

In order to get this working you'll need to create your own Telegram bot (I'd share mine but the Google Translate API isn't free) by following the [instructions here](https://core.telegram.org/bots#6-botfather) then put your API key in a txt file and edit the line that defines `bot_token` in the `main.py` file.  Next you'll need to set up the Google Translate API, the starting point [can be found here.](https://cloud.google.com/translate/), then point the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the JSON file containing your key.

You'll also need to create a file called `bot_token` containing your bot's API token from Telegram, and create an `allowed_ids` file that contains one allowed ID per line.  Only allowed ID's can talk to the bot so this step is important.

Once those files have been created you can run `docker compose up -d --build` to build and run the bot.

If you want it to be able to translate everything said in the group, you'll need change `/setprivacy` to `Disable` by telling @BotFather
