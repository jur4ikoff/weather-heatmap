from fastapi import FastAPI, Body, status, APIRouter, Request, Query, Depends
from fastapi.responses import FileResponse, Response, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


import asyncio
import aiohttp
import os
from dotenv import load_dotenv
import random

from models.geo import Geo
from models.weather import WeatherPoint

from src.geo import GeoManager
from src.osm_map_downloader import OsmMapDownloader, MapDownloaderErrorNotEnoughData, MapDownloaderErrorWhileDownloading
from src.generators import generate_random_name
from src.weather_matrix import WeatherMatrix, WeatherMatrixRequestErr

from heatmap.heatmap import HeatMap

load_dotenv()
IMAGES_PATH = os.getenv("IMAGES_PATH")

STEP_LAT = int(os.getenv("STEP_LAT"))
STEP_LON = int(os.getenv("STEP_LON"))

app = FastAPI()
app.state.cur_proxy = None

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return FileResponse("./templates/index.html")


@app.get("/api/v1.0/heatmap")
async def api_heatmap_v1_0(
    leftdown: str, rightupper: str, width: int = 1280, height: int = 720
):
    """
    str_center_coordinates, in format: lattitude&longitude
    """
    # TODO
    width = 1077
    height = 1280
    # res = await check_proxy(proxy)
    # print(f"proxy res {res}")

    geo_manager = GeoManager()
    try:
        leftdown: Geo = geo_manager.parse_coordinates(
            leftdown)
        rightupper: Geo = geo_manager.parse_coordinates(rightupper)
    except Exception as e:
        print(e)
        return JSONResponse(
            {"message": "Wrong coordinates format"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    valiate_res: bool = geo_manager.validate_coordinates(
        leftdown) and geo_manager.validate_coordinates(rightupper)
    if (not valiate_res):
        return JSONResponse(
            {"message": "Wrong coordinates value"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    map_dowloader = OsmMapDownloader(
        leftdown=leftdown, rightupper=rightupper, width=width, height=height, proxy=app.state.cur_proxy)

    weather_matrix = WeatherMatrix(leftdown, rightupper, width, height)
    weather_request_task = asyncio.create_task(
        weather_matrix.request_weather(STEP_LAT, STEP_LON))

    # filepath = f"{IMAGES_PATH}/{generate_random_name(count=32)}.jpg"
    # download_task = asyncio.create_task(map_dowloader.download_map(filepath))

    # try:
    #     await download_task
    # except MapDownloaderErrorNotEnoughData as e:
    #     return JSONResponse(
    #         {"message": "Loader Enough Data"},
    #         status_code=status.HTTP_502_BAD_GATEWAY,
    #     )
    # except MapDownloaderErrorWhileDownloading as e:
    #     return JSONResponse(
    #         {"message": "Something Went Wrong"},
    #         status_code=status.HTTP_502_BAD_GATEWAY,
    #     )
    # except asyncio.TimeoutError as e:
    #     print(e)
    #     if os.path.exists(filepath):
    #         pass
    #         # return FileResponse(
    #         #     filepath,
    #         #     status_code=status.HTTP_200_OK,
    #         #     headers={
    #         #         "Cache-Control": "no-cache, no-store, must-revalidate",
    #         #         "Pragma": "no-cache",
    #         #         "Expires": "0",
    #         #     },
    #         # )
    #     else:
    #         return JSONResponse(
    #             {"message": "Error, reached timeout load map"},
    #             status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    #         )

    try:
        await weather_request_task
    except WeatherMatrixRequestErr as e:
        print(e)
        return JSONResponse(
            {"message": "Error, not all requests are succesfull"},
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            {"message": "Unexpected exception"},
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        )

    weather_data = weather_matrix.interpolate()
    filepath = "test.jpg"
    heatmap = HeatMap(filepath, weather_data)
    heatmap.get_heatmap()

    # return FileResponse(
    #     filepath,
    #     status_code=status.HTTP_200_OK,
    #     headers={
    #         "Cache-Control": "no-cache, no-store, must-revalidate",
    #         "Pragma": "no-cache",
    #         "Expires": "0",
    #     },
    # )

    return JSONResponse(
        {"message": "Something Went Wrong"},
        status_code=status.HTTP_502_BAD_GATEWAY,
    )
