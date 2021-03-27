#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
from bot import Bot
from pyrogram import filters
from pyrogram.types import Message
from presets import Presets
from init import source_chat, destination_chat


@Bot.on_message(filters.private & filters.command('start'))
async def start_bot(client: Bot, message: Message):
    await message.reply_text(
        text=Presets.WELCOME_TEXT.format(message.from_user.first_name),
        parse_mode='html',
        disable_web_page_preview=True
    )


@Bot.on_message(filters.private & filters.command('help'))
async def help_me(client: Bot, message: Message):
    await message.reply_text(
        text=Presets.HELP_TEXT,
        parse_mode='html',
        disable_web_page_preview=True
    )


@Bot.on_message(filters.private & filters.command('source'))
async def set_source(client: Bot, message: Message):
    ID = int(message.from_user.id)
    if " " in message.text and message.text.split(" ")[1].startswith('-100'):
        source_chat_id = message.text.split(" ")[1]
        if str(source_chat_id).startswith('-100') and source_chat_id[1:].isdigit():
            source_chat[ID] = int(source_chat_id)
            await message.reply_text(
                text=Presets.SOURCE_CONFIRM.format(source_chat_id)
            )
        else:
            await message.reply_text(
                text=Presets.INVALID_CHAT_ID,
                reply_to_message_id=message.message_id
            )
    else:
        await message.reply_text(
            text=Presets.TRY_HELP,
            reply_to_message_id=message.message_id
        )


@Bot.on_message(filters.private & filters.command('destination'))
async def set_destination(client: Bot, message: Message):
    ID = int(message.from_user.id)
    if " " in message.text and message.text.split(" ")[1].startswith('-100'):
        destination_chat_id = message.text.split(" ")[1]
        if str(destination_chat_id).startswith('-100') and destination_chat_id[1:].isdigit():
            destination_chat[ID] = int(destination_chat_id)
            await message.reply_text(
                text=Presets.DESTINATION_CONFIRM.format(destination_chat_id)
            )
        else:
            await message.reply_text(
                text=Presets.INVALID_CHAT_ID,
                reply_to_message_id=message.message_id
            )
    else:
        await message.reply_text(
            text=Presets.TRY_HELP,
            reply_to_message_id=message.message_id
        )


@Bot.on_message(filters.private & filters.command('view'))
async def view(client: Bot, message: Message):
    ID = int(message.from_user.id)
    if ID in source_chat and destination_chat:
        await message.reply_text(
            text=Presets.VIEW_CONF.format(source_chat[ID], destination_chat[ID]),
            reply_to_message_id=message.message_id
        )
    else:
        await message.reply_text(
            text=Presets.NOT_CONFIGURED,
            reply_to_message_id=message.message_id
        )


@Bot.on_message(filters.private & filters.command('delconfig'))
async def del_config(client: Bot, message: Message):
    ID = int(message.from_user.id)
    if ID in source_chat and destination_chat:
        source_chat.pop(ID)
        destination_chat.pop(ID)
        await message.reply_text(
            Presets.CLEAR_CONFIG,
            reply_to_message_id=message.message_id
        )
    else:
        await message.reply_text(
            Presets.NOT_CONFIGURED,
            reply_to_message_id=message.message_id
        )
