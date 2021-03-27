import time
from bot import Bot
from presets import Presets
from pyrogram import filters
from pyrogram.types import Message
from init import source_chat, destination_chat
from pyrogram.errors import FloodWait, ChatAdminRequired
from helper.make_user_join_chat import make_chat_user_join


@Bot.on_message(filters.private & filters.command('clone'))
async def clone_medias(client: Bot, message: Message):
    ID = int(message.from_user.id)
    document = {f'{ID}': 0}
    video = {f'{ID}': 0}
    audio = {f'{ID}': 0}
    if source_chat.keys() and destination_chat.keys():
        try:
            status_message = await client.send_message(
                chat_id=source_chat[ID],
                text=Presets.COPYING_MESSAGES
            )
        except ChatAdminRequired:
            status_message = None
        s__, nop = await make_chat_user_join(
            client.USER,
            status_message
        )
        if not s__:
            if status_message:
                await status_message.edit_text(
                    Presets.IN_CORRECT_PERMISSIONS_MESSAGE.format(
                        nop
                    ),
                    disable_web_page_preview=True
                )
            else:
                await message.delete()
            return
        msg = await client.send_message(
            chat_id=message.chat.id,
            text=Presets.INITIAL_MESSAGE_TEXT,
            disable_notification=True
        )
        async for user_message in client.USER.iter_history(source_chat[ID]):
            messages = await client.get_messages(
                source_chat[ID],
                user_message.message_id,
                replies=0,
            )
            for file_type in tuple(Presets.FILE_TYPES):
                media = getattr(messages, file_type, None)
                if media is not None:
                    if file_type == 'document':
                        document[f'{ID}'] = document[f'{ID}'] + 1
                    elif file_type == 'video':
                        video[f'{ID}'] = video[f'{ID}'] + 1
                    elif file_type == 'audio':
                        audio[f'{ID}'] = audio[f'{ID}'] + 1
                    try:
                        await client.edit_message_text(
                            chat_id=message.chat.id,
                            text=Presets.MESSAGE_COUNT.format(document[f'{ID}'], video[f'{ID}'], audio[f'{ID}']),
                            message_id=msg.message_id
                        )
                    except FloodWait as e:
                        time.sleep(e.x)
                    try:
                        await client.copy_message(
                            chat_id=destination_chat[ID],
                            from_chat_id=source_chat[ID],
                            caption=messages.caption,
                            message_id=messages.message_id,
                            disable_notification=True
                        )
                    except FloodWait as e:
                        time.sleep(e.x)
                    except Exception:
                        await client.send_message(
                            chat_id=message.chat.id,
                            text=Presets.COPY_ERROR_TEXT,
                            reply_to_message_id=message.message_id
                        )
                        return
    else:
        await message.reply_text(
            text=Presets.NOT_CONFIGURED,
            reply_to_message_id=message.message_id
        )
        return
    await message.reply_text(
        text=Presets.FINISHED_TEXT,
        reply_to_message_id=message.message_id,
        parse_mode='html',
        disable_web_page_preview=True
    )
    document.pop(f'{ID}')
    video.pop(f'{ID}')
    audio.pop(f'{ID}')
    source_chat.pop(ID)
    destination_chat.pop(ID)
    await status_message.delete()
    await client.USER.leave_chat(status_message.chat.id)
    return
