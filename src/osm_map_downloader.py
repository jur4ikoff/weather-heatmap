from src.map_downloader import MapDownloader, MapDownloaderErrorNotEnoughData, MapDownloaderErrorWhileDownloading
from src.generators import generate_random_name

from dotenv import load_dotenv
import os

import aiohttp
import aiofiles

import asyncio

load_dotenv()
IMAGES_PATH = os.getenv("IMAGES_PATH")
GEOAPIFY_ACCESS_TOKEN = os.getenv("GEOAPIFY_API_KEY")

scale_diff = 18/20


class OsmMapDownloader(MapDownloader):
    def __init__(self, latitude=None, longitude=None, scale=None, width=1280, height=720):
        super().__init__()
        self.url = "https://staticmap.openstreetmap.de/staticmap.php?"
        self.latitude = latitude
        self.longitude = longitude
        self.scale = scale
        self.width = width
        self.height = height

    async def download_map(self):
        if self.latitude == None or self.longitude == None or self.scale == None:
            return MapDownloaderErrorNotEnoughData()

        print("starting downloading map")
        filepath = f"{IMAGES_PATH}/{generate_random_name(32)}.jpg"
        self.url = "https://maps.geoapify.com/v1/staticmap?"
        params = {
            "apiKey": GEOAPIFY_ACCESS_TOKEN,
            "style": "osm-bright",
            "width": self.width,
            "height": self.height,
            "zoom": self.scale * scale_diff,
            "center": f"lonlat:{self.longitude},{self.latitude}"
        }

        async with aiohttp.ClientSession() as session:
            print(2)
            async with session.get(url=self.url, params=params) as response:
                if (response.status != 200):
                    raise MapDownloaderErrorWhileDownloading()

                print(4)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                print("Starting download")

                async with aiofiles.open(filepath, "wb") as file:
                    async for chunk in response.content.iter_chunked(1024):
                        await file.write(chunk)

        print(f"file saved to {filepath}")
        return filepath
