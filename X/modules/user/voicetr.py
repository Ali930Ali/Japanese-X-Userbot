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




import asyncio
import os

from gtts import gTTS
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER
from config import SUDO_USERS
from X.helpers.basic import edit_or_reply

from .help import *

dil = "id"  # Ses için Varsayılan Dil


@Client.on_message(
    filters.command(["ses", "tts"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def ses(client: Client, message):
    global dil
    cmd = message.command
    if len(cmd) > 1:
        s_metin = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        s_metin = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await edit_or_reply(
            message,
            "**Ses dönüştürmek için mesajlara yanıt verin veya metin argümanları gönderin**",
        )
        return
    await client.send_chat_action(message.chat.id, enums.ChatAction.RECORD_AUDIO)
    # noinspection PyUnboundLocalVariable
    tts = gTTS(s_metin, lang=dil)
    tts.save("ses.mp3")
    if message.reply_to_message:
        await asyncio.gather(
            message.delete(),
            client.send_voice(
                message.chat.id,
                voice="ses.mp3",
                reply_to_message_id=message.reply_to_message.id,
            ),
        )
    else:
        await client.send_voice(message.chat.id, enums.ChatAction.RECORD_AUDIO)
    await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
    os.remove("ses.mp3")


@Client.on_message(filters.me & filters.command(["sesdil"], cmd))
async def sesdil(client: Client, message: Message):
    global dil
    geçici = dil
    dil = message.text.split(None, 1)[1]
    try:
        gTTS("test", lang=dil)
    except Exception:
        await edit_or_reply(message, "Yanlış Dil ID'si!")
        dil = geçici
        return
    await edit_or_reply(
        message, "**Google Ses dili değiştirildi** `{}`".format(dil)
    )


add_command_help(
    "•─╼⃝𖠁 ѕᴇѕ",
    [
        [f"ses veya {cmd}tts [metin/yanıt]", "Metni Google tarafından sese dönüştürür."],
        [
            f"{cmd}sesdil (dil_id) ",
            "Ses dilinizi ayarlayın ve birkaç kullanılabilir ses dilini seçin:"
            "\nID| Dil       | ID| Dil\n"
            "af: Afrikaans | ar: Arapça\n"
            "cs: Çekçe     | de: Almanca\n"
            "el: Yunanca   | en: İngilizce\n"
            "es: İspanyolca| fr: Fransızca\n"
            "hi: Hintçe    | id: Endonezyaca\n"
            "is: İzlandaca | it: İtalyanca\n"
            "ja: Japonca   | jw: Cava Dili\n"
            "ko: Korece    | la: Latince\n"
            "my: Myanmarca | ne: Nepali\n"
            "nl: Hollandaca| pt: Portekizce\n"
            "ru: Rusça     | su: Sundaca\n"
            "sv: İsveççe   | th: Tay Dili\n"
            "tl: Filipince | tr: Türkçe\n"
            "vi: Vietnamca |\n"
            "zh-cn: Çin (Mandarin/Çin)\n"
            "zh-tw: Çin (Mandarin/Tayvan)",
        ],
    ],
)
