# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from telethon import TelegramClient
from telethon.sessions import StringSession

from telethon.errors.rpcerrorlist import MediaEmptyError

from json import loads
from aiofiles import open
from os import environ, path
from veri_ver import a101_brosurler

client = TelegramClient(
    session       = StringSession(),
    api_id        = int(environ.get("TG_API_ID")),
    api_hash      = environ.get("TG_API_HASH")
).start(bot_token = environ.get("TG_BOT_TOKEN"))

async def aktuel_robot():
    if path.isfile('A101.json'):
        async with open("A101.json", "r+", encoding="utf-8") as dosya:
            eski_veriler = loads(await dosya.read())
    else:
        eski_veriler = {}

    yeni_veriler = await a101_brosurler()

    for anahtar in yeni_veriler.keys():
        if (not eski_veriler) or (yeni_veriler[anahtar] != eski_veriler[anahtar]):
            for resim in yeni_veriler[anahtar]:
                if (resim) and (resim not in eski_veriler[anahtar]):
                    try:
                        await client.send_file(int(environ.get("TG_MESAJ_ID")), resim, caption=f"**{anahtar}**")
                    except MediaEmptyError:
                        pass

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(aktuel_robot())
