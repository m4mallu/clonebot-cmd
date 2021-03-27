#----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
from bot import Bot
from pyrogram.types import Message
from pyrogram.errors import InviteHashExpired, InviteHashInvalid, UserAlreadyParticipant

async def make_chat_user_join(client: Bot, message: Message):
    chat_invite_link = await message.chat.export_invite_link()
    try:
        await client.join_chat(chat_invite_link)
    except UserAlreadyParticipant:
        pass
    except (InviteHashExpired, InviteHashInvalid) as e:
        return False, str(e)
    return True, None
