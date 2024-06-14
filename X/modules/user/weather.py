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

# Credits: Athfan Khaleel
# Copyright (C) https://github.com/athphane/userbot
#REMAKE BY NOBITA XD AND TRYTOLIVEALONE 



import asyncio
from html import escape

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums

from X.helpers.basic import edit_or_reply
from config import SUDO_USERS
from .help import *


@Client.on_message(
    filters.command(["weather", "w"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def get_weather(bot: Client, message: Message):
    if len(message.command) == 1:
        await message.edit("Kullanım: `.weather Delhi`")
        await asyncio.sleep(3)
        await message.delete()

    if len(message.command) > 1:
        location = message.command[1]
        headers = {"user-agent": "httpie"}
        url = f"https://wttr.in/{location}?mnTC0&lang=en"
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as resp:
                    data = await resp.text()
        except Exception:
            await message.edit("Hava durumu tahmini alınamadı")

        if "ᴡᴇ ᴘʀᴏᴄᴇꜱꜱᴇᴅ ᴍᴏʀᴇ ᴛʜᴀɴ 𝟷M ʀᴇǫᴜᴇꜱᴛꜱ ᴛᴏᴅᴀʏ" in data:
            await message.edit("`Üzgünüz, bu isteği bugün işleyemiyoruz!`")
        else:
            weather = f"{escape(data.replace('report', 'Report'))}"
            await message.edit(weather, parse_mode=enums.ParseMode.MARKDOWN)


add_command_help(
    "•─╼⃝𖠁 ʜᴀᴠᴀ ᴅᴜʀᴜᴍᴜ",
    [
        [".weather", "Belirtilen konum için hava durumu bilgisini alır."],
    ],
)
