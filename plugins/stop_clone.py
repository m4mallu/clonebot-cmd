import os
import sys
import asyncio
from bot import Bot
from presets import Presets
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

@Client.on_callback_query(filters.regex(r'^stop_clone$'))
async def stop_process(client: Bot, cb: CallbackQuery):
    await cb.message.delete()
    await cb.answer()
    status = await client.send_message(
        chat_id=cb.message.chat.id,
        text=Presets.CANCEL_CLONE,
        reply_to_message_id=cb.message.message_id,
        reply_markup=ReplyKeyboardRemove()
    )
    await asyncio.sleep(3)
    await status.delete()
    await client.send_message(
        chat_id=cb.message.chat.id,
        text=Presets.CANCELLED_MSG,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="CLOSE", callback_data="close_data")]]
        )
    )
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_callback_query(filters.regex(r'^close_data$'))
async def close_button_data(client: Bot, cb: CallbackQuery):
    await cb.answer()
    await cb.message.delete()
