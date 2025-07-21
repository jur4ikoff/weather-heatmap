import asyncio

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

    def set_size(self, width, height):
        self.width = width
        self.height = height

    async def download_map(self):
        if self.latitude == None or self.longitude == None or self.scale == None:
            return MapDownloaderErrorNotEnoughData()

        pass
