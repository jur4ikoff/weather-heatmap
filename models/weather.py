from pydantic import BaseModel

from models.geo import Geo

class WeatherPoint(BaseModel):
    coordinates: Geo
    temperature: float | None