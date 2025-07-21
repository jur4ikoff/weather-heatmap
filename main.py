from fastapi import FastAPI, Body, status, APIRouter, Request, Query
from fastapi.responses import FileResponse, Response, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


import asyncio
import os
from dotenv import load_dotenv
import random

from models.geo import Geo

from src.geo import GeoManager
from src.osm_map_downloader import OsmMapDownloader, MapDownloaderErrorNotEnoughData, MapDownloaderErrorWhileDownloading

load_dotenv()
YANDEX_MAPS_API_KEY: str = os.getenv("YANDEX_MAPS_API_KEY")
# HEATMAP_RADIUS = 10  # 10 км

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return FileResponse("./templates/index.html")


@app.get("/api/v2/heatmap")
async def api_heatmap_v2(
    str_coordinate_1: str, str_coordinate_2: str, scale: int, width: int = 1280, height: int = 720
):
    """Координаты передаются через символ &"""
    geo_manager = GeoManager()
    try:
        coordinates_1: Geo = geo_manager.parse_coordinates(str_coordinate_1)
        coordinates_2: Geo = geo_manager.parse_coordinates(str_coordinate_2)
    except Exception as e:
        return Response(
            {"message": "Fake coordinates"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    validate_res: bool = geo_manager.validate_coordinates(
        coordinates_1) and geo_manager.validate_coordinates(coordinates_2)
    if not validate_res:
        return Response(
            {"message": "No coordinates"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    print(coordinates_1.latitude, coordinates_1.longitude)
    print(coordinates_2.latitude, coordinates_2.longitude)
    print(width, height)

    image_number = random.randint(1, 3)
    image_path = f"./static/images/{image_number}.png"

    return FileResponse(
        image_path,
        status_code=status.HTTP_200_OK,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/api/v1/heatmap")
async def api_heatmap_v1(
    center: str, scale: float, width: int = 1280, height: int = 720
):
    """
    str_center_coordinates, in format: lattitude&longitude
    """
    geo_manager = GeoManager()
    try:
        center: Geo = geo_manager.parse_coordinates(
            center)
    except Exception as e:
        print(e)
        return JSONResponse(
            {"message": "Wrong coordinates format"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    valiate_res: bool = geo_manager.validate_coordinates(center)
    if (not valiate_res):
        return JSONResponse(
            {"message": "Wrong coordinates value"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    map_dowloader = OsmMapDownloader(
        latitude=center.latitude, longitude=center.longitude, scale=scale, width=width, height=height)

    download_task = asyncio.create_task(map_dowloader.download_map())
    filepath: str = await download_task

    # filepath: str = await map_dowloader.download_map()

    return FileResponse(
        filepath,
        status_code=status.HTTP_200_OK,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )


@app.get("/heatmap", response_class=HTMLResponse)
async def get_heatmap(request: Request):
    image_number = random.randint(1, 3)
    image_path = f"/static/images/{image_number}.png"
    return templates.TemplateResponse(
        name="heatmap.html", context={"request": request, "image_path": image_path}
    )
