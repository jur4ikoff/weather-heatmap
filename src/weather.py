import aiohttp
import asyncio

from models.geo import Geo
from models.weather import WeatherPoint


class WeatherGetError(Exception):
    def __init__(self, message=None):
        if message == None:
            self.message = "Error while getting forecast in point"
        else:
            self.message: str = message

    def __str__(self):
        return f"raise Exception, message: {self.message}"


class WeatherManager:
    def __init__(self, proxy=None):
        self.url: str = "https://api.open-meteo.com/v1/forecast?"
        self.proxy = proxy

    def set_proxy(self, proxy):
        self.proxy = proxy

    async def get_weather_in_point(self, point: Geo):
        """Функция возвращает погоду в точке
        https://api.open-meteo.com/v1/forecast?latitude=54.90&longitude=20.90&current=temperature_2m"""

        params = {"latitude": round(point.latitude, 6),
                  "longitude": round(point.longitude, 6),
                  "current": "temperature_2m"}

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
            async with session.get(url=self.url, params=params) as response:
                if (response.status != 200):
                    raise WeatherGetError()

                data = await response.json()
                try:
                    temperature: float = float(
                        data["current"]["temperature_2m"])
                except KeyError as e:
                    print(e)
                    raise WeatherGetError()

        return temperature

    async def get_weather_in_bounds(self, leftdown: Geo, rightupper: Geo) -> list[WeatherPoint]:
        """Функция получает данные в 4 точках риходят в формате "latitide, longitude и возвращает
        массив из 4 точек с погодой. Порядок обхода. Левый верх > Правый верх > Правый низ > Левый низ"""
