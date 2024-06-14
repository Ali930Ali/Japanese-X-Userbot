#MIT License

#Copyright (c) 2024 Japanese-X-Userbot

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

#REMAKE BY NOBITA XD AND TRYTOLIVEALONE



from asyncio import gather
from os import remove

from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from config import CMD_HANDLER
from config import SUDO_USERS
from X.helpers.basic import edit_or_reply
from X.helpers.PyroHelpers import ReplyCheck
from X.utils import extract_user

from .help import *


@Client.on_message(
    filters.command(["whois", "info"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def who_is(client: Client, message: Message):
    user_id = await extract_user(message)
    X = await edit_or_reply(message, "`İşleniyor . . .`")
    if not user_id:
        return await X.edit(
            "**Bu kullanıcının bilgilerini almak için kullanıcı kimliği/kullanıcı adı/yanıt verin.**"
        )
    try:
        user = await client.get_users(user_id)
        username = f"@{user.username}" if user.username else "-"
        first_name = f"{user.first_name}" if user.first_name else "-"
        last_name = f"{user.last_name}" if user.last_name else "-"
        fullname = (
            f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        )
        user_details = (await client.get_chat(user.id)).bio
        bio = f"{user_details}" if user_details else "-"
        h = f"{user.status}"
        if h.startswith("UserStatus"):
            y = h.replace("UserStatus.", "")
            status = y.capitalize()
        else:
            status = "-"
        dc_id = f"{user.dc_id}" if user.dc_id else "-"
        common = await client.get_common_chats(user.id)
        out_str = f"""<b>KULLANICI BİLGİLERİ:</b>

🆔 <b>Kullanıcı ID:</b> <code>{user.id}</code>
👤 <b>Adı:</b> {first_name}
🗣️ <b>Soyadı:</b> {last_name}
🌐 <b>Kullanıcı Adı:</b> {username}
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🤖 <b>Bot mu:</b> <code>{user.is_bot}</code>
🚷 <b>Dolandırıcı mı:</b> <code>{user.is_scam}</code>
🚫 <b>Kısıtlı mı:</b> <code>{user.is_restricted}</code>
✅ <b>Doğrulanmış mı:</b> <code>{user.is_verified}</code>
⭐ <b>Premium mu:</b> <code>{user.is_premium}</code>
📝 <b>Kullanıcı Bio:</b> {bio}

👀 <b>Aynı gruplarda görüldü:</b> {len(common)}
👁️ <b>Son Görülme:</b> <code>{status}</code>
🔗 <b>Kullanıcı kalıcı bağlantısı:</b> <a href='tg://user?id={user.id}'>{fullname}</a>
"""
        photo_id = user.photo.big_file_id if user.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                X.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await X.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await X.edit(f"**BİLGİ:** `{e}`")


@Client.on_message(
    filters.command(["chatinfo", "cinfo", "ginfo"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def chatinfo_handler(client: Client, message: Message):
    X = await edit_or_reply(message, "`İşleniyor...`")
    try:
        if len(message.command) > 1:
            chat_u = message.command[1]
            chat = await client.get_chat(chat_u)
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await message.edit(
                    f"Bu komutu bir grupta kullanın veya `{cmd}chatinfo [grup kullanıcı adı veya id]` kullanın."
                )
            else:
                chatid = message.chat.id
                chat = await client.get_chat(chatid)
        h = f"{chat.type}"
        if h.startswith("ChatType"):
            y = h.replace("ChatType.", "")
            type = y.capitalize()
        else:
            type = "Özel"
        username = f"@{chat.username}" if chat.username else "-"
        description = f"{chat.description}" if chat.description else "-"
        dc_id = f"{chat.dc_id}" if chat.dc_id else "-"
        out_str = f"""<b>GRUP BİLGİLERİ:</b>

🆔 <b>Grup ID:</b> <code>{chat.id}</code>
👥 <b>Başlık:</b> {chat.title}
👥 <b>Kullanıcı Adı:</b> {username}
📩 <b>Tür:</b> <code>{type}</code>
🏛️ <b>DC ID:</b> <code>{dc_id}</code>
🗣️ <b>Dolandırıcı mı:</b> <code>{chat.is_scam}</code>
🎭 <b>Sahte mi:</b> <code>{chat.is_fake}</code>
✅ <b>Doğrulanmış mı:</b> <code>{chat.is_verified}</code>
🚫 <b>Kısıtlı mı:</b> <code>{chat.is_restricted}</code>
🔰 <b>Korunan İçerik:</b> <code>{chat.has_protected_content}</code>

🚻 <b>Toplam Üyeler:</b> <code>{chat.members_count}</code>
📝 <b>Açıklama:</b>
<code>{description}</code>
"""
        photo_id = chat.photo.big_file_id if chat.photo else None
        if photo_id:
            photo = await client.download_media(photo_id)
            await gather(
                X.delete(),
                client.send_photo(
                    message.chat.id,
                    photo,
                    caption=out_str,
                    reply_to_message_id=ReplyCheck(message),
                ),
            )
            remove(photo)
        else:
            await X.edit(out_str, disable_web_page_preview=True)
    except Exception as e:
        return await X.edit(f"**BİLGİ:** `{e}`")


add_command_help(
    "•─╼⃝𖠁 Bilgi",
    [
        [
            "info <kullanıcı adı/kullanıcı kimliği/yanıt>",
            "Telegram kullanıcı bilgilerini tam açıklama ile alın.",
        ],
        [
            "chatinfo <kullanıcı adı/grup kimliği/yanıt>",
            "Grup bilgilerini tam açıklama ile alın.",
        ],
    ],
)
