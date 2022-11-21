# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from aiocfscrape import CloudflareScraper
from parsel      import Selector
from aiofiles    import open
from json        import dumps

async def kaynaktan_listeye(kaynak_kod:str) -> list[str]:
    secici = Selector(kaynak_kod)
    return [resim.xpath("./@src").get() for resim in secici.xpath("//div[@class='view-area']//img")]

async def a101_brosurler() -> dict[str, str]:
    domain = "https://www.a101.com.tr"

    brosurler = {}
    async with CloudflareScraper() as oturum:
        async with oturum.get(f"{domain}/aldin-aldin-bu-hafta-brosuru") as yanit:
            if yanit.status != 200:
                print(await yanit.text())
                brosurler["Bu Hafta"] = None
            else:
                brosurler["Bu Hafta"] = await kaynaktan_listeye(await yanit.text())

        async with oturum.get(f"{domain}/aldin-aldin-gelecek-hafta-brosuru") as yanit:
            if yanit.status != 200:
                print(await yanit.text())
                brosurler["Gelecek Hafta"] = None
            else:
                brosurler["Gelecek Hafta"] = await kaynaktan_listeye(await yanit.text())

        async with oturum.get(f"{domain}/afisler-haftanin-yildizlari") as yanit:
            if yanit.status != 200:
                print(await yanit.text())
                brosurler["Haftanın Yıldızları"] = None
            else:
                brosurler["Haftanın Yıldızları"] = await kaynaktan_listeye(await yanit.text())

        async with oturum.get(f"{domain}/buyuk-oldugu-icin-ucuz-afisler") as yanit:
            if yanit.status != 200:
                print(await yanit.text())
                brosurler["Büyük olduğu için UCUZ"] = None
            else:
                brosurler["Büyük olduğu için UCUZ"] = await kaynaktan_listeye(await yanit.text())

    async with open("A101.json", "w+", encoding="utf-8") as dosya:
        await dosya.write(dumps(brosurler, indent=2, ensure_ascii=False, sort_keys=False))

    return brosurler