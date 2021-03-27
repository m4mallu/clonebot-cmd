# [Clone Bot](https://github.com/m4mallu/clonebot)

#### A simple telegram bot to clone Medias from one chat to another

Note: 
- Bot need to be an admin of the source and destination Chats.
- String session user doesn't need to be an admin of both ends.
- String session user should not be banned in the source chat.

### Requirements:
```
TG_BOT_TOKEN    - Get from @BotFather
APP_ID          - Get from my.telegram.org
API_HASH        - Get from my.telegram.org
TG_USER_SESSION - Run any userbot session maker(https://repl.it/@ayrahikari/pyrogram-session-maker)
```

### @BotFather Command:
```
/help - To know how to use the bot

/source - Set source chat Id ( /source -1001234567890 )

/destination - Set destination chat Id ( /destination -1009876543210)

/view - To view the current stored chat configuration

/delconfig - To clear the stored chat configuration

/clone - Clone medias from source to destination chat

```
### Deploy Easy Way:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/m4mallu/clonebot)

### Deploy Hard Way:

Create **config.py** with variables as given below [Refer sample.config](https://github.com/m4mallu/clonebot/blob/master/sample_config.py)

```
class Config(object):
    TG_BOT_TOKEN = "134448596:AAEIyo3EBVCN3qdd3TfrmQUxoI-eZVGvmI"
    APP_ID = int(123635)
    API_HASH = "1a417dd4fdf3ead2819ff35641daa16b"
    TG_USER_SESSION = "BQDGRUC0_qw2GVQ2gpLFaXOt0mrWg16cBZPATQvR8KThDzi-NRE1I9DB......"
```
[User session string can be generated from HERE](https://replit.com/@ayrahikari/pyrogram-session-maker)

#### Run the following:

```
virtualenv -p python3 venv
. ./venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

### LICENSE

- [GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

### Credits:

[DAN](https://t.me/haskell) for his [Pyrogram](https://github.com/pyrogram/pyrogram) Library

[SpEcHiDe](https://github.com/SpEcHiDe) for his [DeleteMessagesRoBot](https://github.com/SpEcHiDe/DeleteMessagesRoBot)

### Creator :

[Mallu Boy](https://t.me/m4mallu) In Telegram - [AS](https://t.me/space4renjith)