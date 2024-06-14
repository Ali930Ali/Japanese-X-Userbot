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



from asyncio import sleep
from contextlib import suppress
from random import randint
from typing import Optional

from pyrogram import Client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message

from config import CMD_HANDLER
from config import SUDO_USERS
from X.helpers.adminHelpers import DEVS
from X.helpers.basic import edit_or_reply
from X.helpers.tools import get_arg

from .help import *


async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"**Grup çağrısı bulunamadı** {err_msg}")
    return False


@Client.on_message(
    filters.command("Başlatvc", [""]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["başlatvc"], cmd) & filters.me)
@Client.on_message(
    filters.command(["başlatvc"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    X = await edit_or_reply(message, "`İşleniyor . . .`")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = f"**Grup Çağrısı Başlatıldı\n • **Chat ID** : `{chat_id}`"
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • **Başlık:** `{vctitle}`"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await X.edit(args)
    except Exception as e:
        await X.edit(f"**BİLGİ:** `{e}`")


@Client.on_message(filters.command("Durdurvc", [""]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["durdurvc"], cmd) & filters.me)
@Client.on_message(
    filters.command(["durdurvc"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def end_vc_(client: Client, message: Message):
    """Grup çağrısını bitir"""
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(client, message, err_msg=", grup çağrısı zaten bitti")
        )
    ):
        return
    await client.send(DiscardGroupCall(call=group_call))
    await edit_or_reply(message, f"Grup çağrısı sona erdi **Chat ID** : `{chat_id}`")


@Client.on_message(
    filters.command("naikos", [""]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(
    filters.command(["naikos"], ".") & (filters.me | filters.user(SUDO_USERS))
)
@Client.on_message(filters.command("katılvc", cmd) & filters.me)
@Client.on_message(
    filters.command(["katılvc"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def joinvc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        X = await message.reply("`Katılmayı Deniyor...`")
    else:
        X = await message.edit("`İşleniyor...`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.start(chat_id)
    except Exception as e:
        return await X.edit(f"**HATA:** `{e}`")
    await X.edit(f"❏ **Başarıyla Sesli Sohbete Katıldı**\n└ **Chat ID:** `{chat_id}`")
    await sleep(5)
    await client.group_call.set_is_mute(True)


@Client.on_message(
    filters.command("turunos", [""]) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("ayrılvc", cmd) & filters.me)
@Client.on_message(
    filters.command(["ayrılvc"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def leavevc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        X = await message.reply("`Önce aşağı inin, çocuklar...`")
    else:
        X = await message.edit("`İşleniyor...`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.stop()
    except Exception as e:
        return await edit_or_reply(message, f"**HATA:** `{e}`")
    msg = "❏ **Doğa çağrısından dolayı Tod'un Mağarasından çıkıyor**"
    if chat_id:
        msg += f"\n└ **Chat ID:** `{chat_id}`"
    await X.edit(msg)


add_command_help(
    "•─╼⃝𖠁 ѕᴇѕʟɪ ᴋᴏɴᴜşᴍᴀ ᴛᴏᴏʟ'ʟᴀʀɪ",
    [
        ["başlatvc", "Grupta Sesli Sohbeti Başlatın."],
        ["durdurvc", "Grupta Sesli Sohbeti Durdurun."],
        [
            f"katılvc veya {cmd}katılvc <chatid/kullanıcı adı>",
            "Grupta Sesli Sohbete Katılın.",
        ],
        [
            f"ayrılvc veya {cmd}ayrılvc <chatid/kullanıcı adı>",
            "Grupta Sesli Sohbetten Ayrılın.",
        ],
    ],
)
