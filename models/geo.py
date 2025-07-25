from pydantic import BaseModel


class Geo(BaseModel):
    latitude: float
    longitude: float

    def __str__(self):
        return f"({round(self.latitude, 5)},{round(self.longitude, 5)})"
