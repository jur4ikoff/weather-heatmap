from src.map_downloader import MapDownloader, MapDownloaderErrorNotEnoughData, MapDownloaderErrorWhileDownloading

from models.geo import Geo

from dotenv import load_dotenv
import os

import aiohttp
import aiofiles


load_dotenv()
GEOAPIFY_ACCESS_TOKEN = os.getenv("GEOAPIFY_API_KEY")


proxy = "http://93.190.138.107:46182"


class OsmMapDownloader(MapDownloader):
    def __init__(self, leftdown: Geo, rightupper: Geo, width=1280, height=720):
        super().__init__()
        self.url = "https://staticmap.openstreetmap.de/staticmap.php?"
        self.leftdown: Geo = leftdown
        self.rightupper: Geo | None = rightupper
        self.width = width
        self.height = height

    async def download_map(self, filepath: str) -> bool:
        if self.leftdown == None or self.rightupper == None:
            return MapDownloaderErrorNotEnoughData()

        print("starting downloading map")
        self.url = "https://maps.geoapify.com/v1/staticmap?"
        params = {
            "apiKey": GEOAPIFY_ACCESS_TOKEN,
            "style": "dark-matter-brown",
            "width": self.width,
            "height": self.height,
            "area": f"rect:{self.leftdown.longitude},{self.leftdown.latitude},{self.rightupper.longitude},{self.rightupper.latitude}"
        }

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
            async with session.get(url=self.url, params=params, proxy=proxy) as response:
                if (response.status != 200):
                    raise MapDownloaderErrorWhileDownloading()

                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                print("Starting download")

                async with aiofiles.open(filepath, "wb") as file:
                    async for chunk in response.content.iter_chunked(1024):
                        await file.write(chunk)

        print(f"file saved to {filepath}")
        return True
