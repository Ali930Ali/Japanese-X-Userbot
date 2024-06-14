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


#CREDIT : NOBITA XD
#DON'T KANG FUCKING COWARD
#BSDKE KANG KIYA TOH SOCH LIYO
#AAG LAGA DUNGA TERE ANDAR 
#SAMJHA ? 


import reportlab
from pyrogram import Client, filters
from pyrogram.types import Message
from config import SUDO_USERS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .help import * 


@Client.on_message(
    filters.command(["kullanicilistesi"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def generate_user_list_pdf(client: Client, message: Message):
    chat_id = message.chat.id
    members = await client.get_chat_members(chat_id)
    
    c = canvas.Canvas("kullanici_listesi.pdf", pagesize=letter)
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Kullanıcı Listesi:")
    
    y_position = 730
    for member in members:
        user = member.user
        user_info = f"{user.first_name} {user.last_name or ''} - @{user.username or ''}"
        c.drawString(100, y_position, user_info)
        y_position -= 20
    
    c.save()

    await client.send_document(chat_id, "kullanici_listesi.pdf")


add_command_help(
    "•─╼⃝𖠁 Kᴜʟʟᴀɴɪᴄɪʟɪsᴛᴇsɪ",
    [
       ["kullanicilistesi", "Bu sohbetteki kullanıcı listesini gönderir."],
    ],
)
