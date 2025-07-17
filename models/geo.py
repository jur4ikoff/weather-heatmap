from pydantic import BaseModel

class Geo(BaseModel):
    latitude : float
    longitude : float