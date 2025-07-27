import asyncio
import aiohttp
import aiofiles
import os

IMAGES_DIRECTORY = "static/images/"


class MapDownloaderErrorNotEnoughData(Exception):
    def __init__(self, message=None):
        if message == None:
            self.message = "Error, not enough data to make request to static map api"
        else:
            self.message: str = message

    def __str__(self):
        return f"raise Exception, message: {self.message}"


class MapDownloaderErrorWhileDownloading(Exception):
    def __init__(self, message=None):
        if message == None:
            self.message : str = "Error while downloading"
        else:
            self.message: str = message

    
    def __str__(self):
        return f"raise Exception, message: {self.message}"

class MapDownloader:
    def __init__(self, latitude=None, longitude=None, scale=None, width=1280, height=720):
        self.latitude: float | None = latitude
        self.longitude: float | None = longitude
        self.scale: float | None = scale
        self.width: int | None = width
        self.height: int | None = height

        self.params = None
        self.url = None

    def set_size(self, width, height):
        self.width = width
        self.height = height

    async def download_map(self, filepath: str) -> bool:
        # if self.leftdown == None or self.rightupper == None:
        #     return MapDownloaderErrorNotEnoughData()

        print("starting downloading map")

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
            async with session.get(url=self.url, params=self.params) as response:
                if (response.status != 200):
                    raise MapDownloaderErrorWhileDownloading()

                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                print("Starting download")

                async with aiofiles.open(filepath, "wb") as file:
                    async for chunk in response.content.iter_chunked(1024):
                        await file.write(chunk)

        print(f"file saved to {filepath}")
        return True
