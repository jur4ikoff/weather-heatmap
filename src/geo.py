from models.geo import Geo


class GeoManager:
    """Класс, отвечает за работк с координатами"""

    def __init__(self):
        pass

    @staticmethod
    def parse_coordinates(coordinates: str) -> Geo:
        """Парсит строку, в которой содержатся координаты в формате (firstcoordinate&secondcoordinate)"""
        latitude, longitude = list(map(float, coordinates.split("&")))
        return Geo(latitude=latitude, longitude=longitude)

    @staticmethod
    def validate_coordinates(coordinates: Geo) -> bool:
        if coordinates.latitude < -90 or coordinates.latitude > 90:
            return False

        if coordinates.longitude < -180 or coordinates.longitude > 180:
            return False

        return True
