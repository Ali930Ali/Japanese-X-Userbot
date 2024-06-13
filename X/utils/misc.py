# MIT Lisansı

# Telif Hakkı (c) 2024 Japanese-X-Userbot

# Bu yazılım ve ilişkili belge dosyalarının (bundan böyle "Yazılım" olarak anılacaktır) herhangi bir kişiye ücretsiz olarak verilmesine izin verilir,
# bu yazılımı kısıtlama olmaksızın kullanma, kopyalama, değiştirme, birleştirme, yayınlama, dağıtma, alt lisanslama ve/veya satma
# kopyaları ve yazılımı alan kişilere bu yazılımı kullanma izni verilir, ancak aşağıdaki koşullara tabidir:

# Yukarıdaki telif hakkı bildirimi ve bu izin bildirimi tüm kopyalar veya önemli kısımlarında bulunmalıdır.

# YAZILIM "OLDUĞU GİBİ" SAĞLANIR, HİÇBİR TÜRDE GARANTİ VERİLMEMEKTEDİR, AÇIK VEYA
# ZIMNİ, SATILABİLİRLİK, BELİRLİ BİR AMACA UYGUNLUK VEYA İHLAL KONUSUNDA GARANTİLER DAHİL
# OLMAK ÜZERE, FAKAT BUNLARLA SINIRLI OLMAKSIZIN, HİÇBİR GARANTİ VERİLMEMEKTEDİR. HERHANGİ BİR DURUMDA
# YAZARLAR VEYA TELİF HAKKI SAHİPLERİNDEN HERHANGİ BİR TALEP, ZARAR VEYA DİĞER
# SORUMLULUK, SÖZLEŞME DAVA, HAKSIZ FİİL VEYA BAŞKA BİR SEBEP İLE, YAZILIMIN KULLANILMASINDAN,
# YAZILIMLA BAĞLANTILI OLARAK VEYA BAŞKA TÜRLÜ, ORTAYA ÇIKMAMALIDIR.

import socket
from asyncio import get_running_loop
from functools import partial
import os
import sys
from re import sub
from time import time

from pyrogram import Client, enums

admins_in_chat = {}


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()

async def is_heroku():
    return "heroku" in socket.getfqdn()


async def user_input(input):
    if " " in input or "\n" in input:
        return str(input.split(maxsplit=1)[1].strip())
    return ""

async def paste_queue(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(
        None, partial(_netcat, "ezup.dev", 9999, content)
    )
    return link


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "X"])


async def list_admins(client: Client, chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]


async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True

    text = text.strip()

    if is_int(text):
        return int(text)

    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None


async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]


async def extract_args(message, markdown=True):
    if not (message.text or message.caption):
        return ""

    text = message.text or message.caption

    text = text.markdown if markdown else text
    if " " not in text:
        return ""

    text = sub(r"\s+", " ", text)
    text = text[text.find(" ") :].strip()
    return text


async def extract_args_arr(message, markdown=True):
    return extract_args(message, markdown).split()
