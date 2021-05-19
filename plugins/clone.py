#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import time
import pytz
import datetime
import asyncio
from bot import Bot
from presets import Presets
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from init import source_chat, destination_chat
from pyrogram.errors import FloodWait

bot_start_time = time.time()

@Bot.on_message(filters.private & filters.command('clone'))
async def clone_medias(client: Bot, message: Message):
    ID = int(message.from_user.id)

    clone_start_time = time.time()
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')

    doc_files = 0
    video_files = 0
    audio_files = 0

    if ID in source_chat and destination_chat:
        user_bot_me = await client.USER.get_me()
        msg = await client.send_message(
            chat_id=message.chat.id,
            text=Presets.INITIAL_MESSAGE_TEXT,
            disable_notification=True
        )
        msg1 = await client.send_message(
            chat_id=message.chat.id,
            text=Presets.WAIT_MSG
        )
        # Checking string session user is in the given source chat id as self
        try:
            await client.USER.get_chat_member(chat_id=source_chat[ID], user_id=user_bot_me.id)
        except Exception:
            await msg1.delete()
            await msg.edit(
                text=Presets.IN_CORRECT_PERMISSIONS_MESSAGE,
            )
            source_chat.pop(ID)
            destination_chat.pop(ID)
            return
        try:
            await msg1.edit(
                text=Presets.CLOSE_BTN_TXT,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="🌀 CANCEL 🌀", callback_data="stop_clone")]]
                    )
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception:
            pass
        async for user_message in client.USER.iter_history(source_chat[ID]):
            messages = await client.USER.get_messages(
                source_chat[ID],
                user_message.message_id,
                replies=0,
            )
            time_taken = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - clone_start_time))
            uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - bot_start_time))
            update = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S %p')
            for file_type in tuple(Presets.FILE_TYPES):
                media = getattr(messages, file_type, None)
                if media is not None:
                    if file_type == 'document':
                        doc_files += 1
                    elif file_type == 'video':
                        video_files += 1
                    elif file_type == 'audio':
                        audio_files += 1
                    else:
                        pass
                    try:
                        await msg.edit(
                            text=Presets.MESSAGE_COUNT.format(
                                doc_files,
                                video_files,
                                audio_files,
                                time_taken,
                                uptime,
                                current_time,
                                update
                            )
                        )
                        await asyncio.sleep(1)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                    except Exception:
                        pass
                    try:
                        await client.USER.copy_message(
                            chat_id=destination_chat[ID],
                            from_chat_id=source_chat[ID],
                            caption=messages.caption,
                            message_id=messages.message_id,
                            disable_notification=True
                        )
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                    except Exception:
                        # Clone error due to string session user is not an admin of the given destination chat !
                        await msg1.delete()
                        await msg.edit(Presets.COPY_ERROR_TEXT)
                        source_chat.pop(ID)
                        destination_chat.pop(ID)
                        return
    else:
        await message.reply_text(Presets.NOT_CONFIGURED)
        return
    await msg1.edit(Presets.FINISHED_TEXT)
    source_chat.pop(ID)
    destination_chat.pop(ID)
    return
