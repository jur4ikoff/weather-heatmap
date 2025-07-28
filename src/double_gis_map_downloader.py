from src.map_downloader import MapDownloader, MapDownloaderErrorNotEnoughData, MapDownloaderErrorWhileDownloading

from models.geo import Geo
import math


class DoubleGisMapDownloader(MapDownloader):
    def __init__(self, leftdown: Geo, rightupper: Geo, width, height):
        super().__init__()
        self.url = "https://static.maps.2gis.com/1.0?"

        lat = (leftdown.latitude + rightupper.latitude) / 2
        lon = (leftdown.longitude + rightupper.longitude) / 2

        zoom = self.calculate_zoom(leftdown, rightupper, width, height)

        self.params = {
            "s": f"{width}x{height}",
            "c": f"{lat},{lon}",
            "z": zoom
        }

    def calculate_zoom(self, leftdown: Geo, rigthupper: Geo, width, height):
        # Разница в долготе и широте
        lat_diff = math.fabs(rigthupper.latitude -
                             leftdown.latitude)  # широта (Y)
        lon_diff = math.fabs(rigthupper.longitude -
                             leftdown.longitude)  # долгота (X)

        # Рассчитываем zoom по ширине и высоте
        zoom_lon = math.log2(360 * int(width) / (128 * lon_diff))
        zoom_lat = math.log2(180 * int(height) / (128 * lat_diff))

        # Выбираем минимальный zoom, чтобы вся область влезла
        zoom = min(zoom_lon, zoom_lat)

        # Ограничиваем zoom (обычно 1-20)
        return max(1, min(20, int(zoom)))
