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

import aiohttp
import requests

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def PasteBin(text):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link


async def paste(content: str):
    resp = await post(f"{BASE}api/v2/paste", data=content)
    if not resp["success"]:
        return
    return BASE + resp["message"]


async def s_paste(message, extension="txt"):
    siteurl = "https://spaceb.in/api/v1/documents/"
    try:
        response = requests.post(
            siteurl, data={"content": message, "extension": extension}
        )
    except Exception as e:
        return {"error": str(e)}
    if response.ok:
        response = response.json()
        if response["error"] != "" and response["status"] < 400:
            return {"error": response["error"]}
        return {
            "url": f"https://spaceb.in/{response['payload']['id']}",
            "raw": f"{siteurl}{response['payload']['id']}/raw",
            "bin": "Spacebin",
        }
    return {"error": "Spacebin'e erişilemedi."}
    
