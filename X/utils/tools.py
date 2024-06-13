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

import asyncio
import os
import shlex
import textwrap
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

absen = [
    "**Geliyorum kardeş** 😁",
    "**Varım kız kardeş** 😉",
    "**Orada olacağım, lütfen** 😁",
    "**Varım yakışıklı** 🥵",
    "**Varım kardeş** 😎",
    "**Daha sonra yok**",
    "**Buradayım, geç kaldığım için özür dilerim** 🥺",
]


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["sn", "dk", "saat", "gün"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


async def add_text_img(image_path, text):
    font_size = 12
    stroke_width = 1

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="X/resources/default.ttf",
        size=int(image_height * font_size) // 100,
    )
    draw = ImageDraw.Draw(img)

    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    if top_lines:
        y = 10
        for line in top_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    if bottom_lines:
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    final_image = os.path.join("memify.webp")
    img.save(final_image, **img_info)
    return final_image


# https://github.com/TeamUltroid/pyUltroid/blob/31c271cf4d35ab700e5880e952e54c82046812c2/pyUltroid/functions/helper.py#L154


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
            )
        
