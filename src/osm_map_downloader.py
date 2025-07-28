from src.map_downloader import MapDownloader, MapDownloaderErrorNotEnoughData, MapDownloaderErrorWhileDownloading

from models.geo import Geo

from dotenv import load_dotenv
import os



load_dotenv()
GEOAPIFY_ACCESS_TOKEN = os.getenv("GEOAPIFY_API_KEY")


class OsmMapDownloader(MapDownloader):
    def __init__(self, leftdown: Geo, rightupper: Geo, width, height):
        super().__init__()
        self.url = "https://staticmap.openstreetmap.de/staticmap.php?"
        self.leftdown: Geo = leftdown
        self.rightupper: Geo | None = rightupper
        self.width = width
        self.height = height

        self.url = "https://maps.geoapify.com/v1/staticmap?"

        self.params = {
            "apiKey": GEOAPIFY_ACCESS_TOKEN,
            "style": "dark-matter-brown",
            "width": self.width,
            "height": self.height,
            "area": f"rect:{self.leftdown.longitude},{self.leftdown.latitude},{self.rightupper.longitude},{self.rightupper.latitude}"
        }


