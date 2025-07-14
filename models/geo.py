from pydantic import BaseModel

class Geo(BaseModel):
    latitude : str
    longitude : str