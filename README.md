[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white) ![dependabot auto-merging](https://github.com/v1nsai/the_interpreter_bot/actions/workflows/dependabot.yml/badge.svg)

# The Interpreter: A Telegram Bot
<img src="https://github.com/v1nsai/the_interpreter_bot/assets/410443/205a8e6f-b361-4913-b500-fe7a81d9592b" width=256 height=256 />

## Prerequisites
### Create a Telegram bot
* Create a telegram bot by following the [instructions here](https://core.telegram.org/bots#6-botfather).
* Disable privacy on the bot to allow it to see the contents of your chat using `/setprivacy disable`
* Create a file called `bot_token` in the project root and add your telegram bot's API token to it.
### Create a Google project and service account
* Create a Google project that uses the Translate API, the starting point [can be found here.](https://cloud.google.com/translate/).
* Create a service account with permission to use the Translate API, and create an API key.  Download the JSON file to the project root and call it `google_key.json`.
### Create group chats to use your bot (groups must be whitelisted before use)
* Create a Telegram group chat that you want to invite your bot to.  Invite `@getidsbot` to the chat, and it will immediately give you lots of info, including the group chat ID.  Add that ID and any others you want to talk to your bot in to a file called `allowed_ids` at the project root.  One ID per line.

## Installation
Once you've set up the `bot_token`, `google_key.json` and `allowed_ids` files, run `docker compose up -d --build` to bring it all online
