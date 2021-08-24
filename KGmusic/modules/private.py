# Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from KGmusic.modules.msg import Messages as tr
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from KGmusic.config import SOURCE_CODE,ASSISTANT_NAME,PROJECT_NAME,SUPPORT_GROUP,UPDATES_CHANNEL,BOT_USERNAME, OWNER, BOT_NAME
logging.basicConfig(level=logging.INFO)
from KGmusic.helpers.filters import command
from pyrogram import Client, filters
from time import time
from datetime import datetime
from KGmusic.helpers.decorators import authorized_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

@Client.on_message(
    filters.command("start")
    & filters.private
    & ~ filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋 **ʜᴀʟʟᴏ** **{message.from_user.first_name}**\n
🤖 **[{BOT_NAME}](https://t.me/{BOT_USERNAME})** ᴀᴋᴀɴ ᴍᴇᴍʙᴀɴᴛᴜ ᴋᴀʟɪᴀɴ ᴜɴᴛᴜᴋ ᴍᴇʀɪᴀʜᴋᴀɴ ɢʀᴜᴘ ᴋᴀʟɪᴀɴ!!

⚠️ ᴊɪᴋᴀ ᴋᴀʟɪᴀɴ ᴛɪᴅᴀᴋ ᴍᴇɴɢᴇʀᴛɪ ᴛᴇɴᴛᴀɴɢ {BOT_NAME} sɪʟᴀᴋᴀɴ ᴋʟɪᴄᴋ » 📚 ᴄᴏᴍᴍᴀɴᴅs «

❓ ᴜɴᴛᴜᴋ ɪɴғᴏʀᴍᴀsɪ ᴋᴇsᴇʟᴜʀᴜʜᴀɴ ᴛᴇɴᴛᴀɴɢ {BOT_NAME} sᴇʟᴇɴɢᴋᴀᴘɴʏᴀ » /help «
<b>""",

        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʏᴀ ᴋᴇ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
                [
                    InlineKeyboardButton(
                        "ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"), 
                    InlineKeyboardButton(
                        "ɢʀᴏᴜᴘ", url=f"https://t.me/{SUPPORT_GROUP}")
                ],[
                    InlineKeyboardButton(
                        "ᴄʀᴇᴀᴛᴇᴅ ʙʏ", url=f"https://t.me/{OWNER}")
                ],[
                    InlineKeyboardButton(
                        "📚 ᴄᴏᴍᴍᴀɴᴅs", url=f"https://telegra.ph/KG-Music-08-23")
                ],[
                    InlineKeyboardButton(
                        "•ʀᴇᴘᴏ", url=f"https://github.com/kgproject1010/KG-Music")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
        )

@Client.on_message(filters.private & filters.incoming & filters.command(['help']))
def _help(client, message):
    client.send_message(chat_id = message.chat.id,
        text = tr.HELP_MSG[1],
        parse_mode="markdown",
        disable_web_page_preview=True,
        disable_notification=True,
        reply_markup = InlineKeyboardMarkup(map(1)),
        reply_to_message_id = message.message_id
    )

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))

@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    disable_web_page_preview=True
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split('+')[1])
    client.edit_message_text(chat_id=chat_id,    message_id=message_id,
        text=tr.HELP_MSG[msg],    reply_markup=InlineKeyboardMarkup(map(msg))
    )


def map(pos):
    if(pos==1):
        button = [
            [InlineKeyboardButton(text = 'ɴᴇxᴛ »', callback_data = "help+2")]
        ]
    elif(pos==len(tr.HELP_MSG)-1):
        url = f"https://t.me/KGSupportgroup"
        button = [
            [InlineKeyboardButton("➕ Tambahkan saya ke grup anda ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton(text = 'ᴄʜᴀɴɴᴇʟ', url=f"https://t.me/rakasupport"),
             InlineKeyboardButton(text = 'ɢʀᴏᴜᴘ', url=f"https://t.me/KGSupportgroup")],
            [InlineKeyboardButton(text = 'ᴅᴇᴠᴇʟᴏᴘᴇʀ', url=f"https://t.me/knsgnwn")]
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text = '«', callback_data = f"help+{pos-1}"),
                InlineKeyboardButton(text = '»', callback_data = f"help+{pos+1}")
            ],
        ]
    return button


@Client.on_message(
    filters.command("start")
    & filters.group
    & ~ filters.edited
)
async def start(client: Client, message: Message):
    await message.reply_text(
        "**Apakah anda ingin mencari link YouTube?**",
        reply_markup=InlineKeyboardMarkup(
            [   
                [    
                    InlineKeyboardButton(
                        "✅ Ya", switch_inline_query_current_chat=""
                    ),
                    InlineKeyboardButton(
                        "❌ Tidak ", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_message(
    filters.command("help")
    & filters.group
    & ~ filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        """baca panduan bot dibawah ini""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📚 ᴘᴀɴᴅᴜᴀɴ ʙᴏᴛ", url="https://telegra.ph/KG-Music-08-23"
                    )
                ]
            ]
        ),
    )  


@Client.on_message(
    filters.command("reload")
    & filters.group
    & ~ filters.edited
)
async def reload(client: Client, message: Message):
    await message.reply_text("""⚙️ ʙᴏᴛ **ʙᴇʀʜᴀsɪʟ ᴅɪᴍᴜᴀᴛ ᴜʟᴀɴɢ!**\n\n• **ᴅᴀғᴛᴀʀ ᴀᴅᴍɪɴ** ᴛᴇʟᴀʜ **ᴅɪᴘᴇʀʙᴀʀᴜɪ**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ɢʀᴏᴜᴘ", url=f"https://t.me/KGSupportgroup"
                    ),
                    InlineKeyboardButton(
                        "ᴄʀᴇᴀᴛᴇᴅ ʙʏ", url=f"https://t.me/knsgnwn"
                    )
                ]
            ]
        )
   )

@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("ᴘɪɴɢɪɴɢ...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🏓 `PONG!!`\n"
        f"⚡️ `{delta_ping * 1000:.3f} ᴍs`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@authorized_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• 🚀 **ᴜᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"• ⚡ **sᴛᴀʀᴛ ᴛɪᴍᴇ:** `{START_TIME_ISO}`"
    )
