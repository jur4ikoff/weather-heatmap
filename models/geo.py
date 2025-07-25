from pydantic import BaseModel

class Geo(BaseModel):
    latitude : float
    longitude : float

    def __str__(self):
        return f"coords={self.latitude},{self.longitude}"