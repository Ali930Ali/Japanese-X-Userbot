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

import asyncio
import re

from pyrogram import filters, Client
from pyrogram.errors import MessageNotModified
from pyrogram.types import Message
from config import SUDO_USERS

from .help import *

kötü_kelimeler = ["zenci", "zenciler", "maymun", "gerizekalı", "siktir", "orospu çocuğu"]

kaba_filtresi = True


def değiştir():
    global kaba_filtresi
    kaba_filtresi = not kaba_filtresi
    return kaba_filtresi


@Client.on_message(
    filters.command(["kaba"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def geçiş(bot: Client, message: Message):
    c = değiştir()
    await message.edit("`Kaba Filtresi Etkin`" if c else "`Kaba Filtresi Devre Dışı`")
    await asyncio.sleep(3)
    await message.delete()


@Client.on_message(~filters.regex(r"^\.\w*") & filters.me & ~filters.media, group=10)
async def bunu_söylememe_izin_yok(bot: Client, message: Message):
    if kaba_filtresi:
        try:
            metin = None
            if message.caption:
                metin = message.caption
            elif message.text:
                metin = message.text

            for kelime in kötü_kelimeler:
                try:
                    metin = re.sub(kelime, "ahbap", metin, flags=re.IGNORECASE)
                except Exception as e:
                    print(f"{e}")

            if message.caption:
                if metin != message.caption:
                    await message.edit_caption(metin)

            elif message.text:
                if metin != message.text:
                    await message.edit(metin)
        except MessageNotModified:
            return


add_command_help(
    "•─╼⃝𖠁 ᴋᴀʙᴀ",
    [
        [".kaba", "Kötü kelime filtresini açar ve kapatır."],
    ],
)
