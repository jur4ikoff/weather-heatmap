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
from src.double_gis_map_downloader import DoubleGisMapDownloader
from src.generators import generate_random_name
from src.weather_matrix import WeatherMatrix, WeatherMatrixRequestErr

from heatmap.heatmap import HeatMap, HetmapDataEmptyException, HeatmapFileNotFoundException, HeatmapErrImageException


load_dotenv()
IMAGES_PATH = os.getenv("IMAGES_PATH")

STEP_LAT = int(os.getenv("STEP_LAT"))
STEP_LON = int(os.getenv("STEP_LON"))

app = FastAPI()
app.state.cur_proxy = "http://109.191.0.92:8081"

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")
app.mount("/styles", StaticFiles(directory="styles"), name="styles")

templates = Jinja2Templates(directory="templates")


async def check_proxy(proxy):
    test_url = "https://httpbin.org/ip"  # Сервис, который возвращает ваш IP
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(test_url, proxy=proxy, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Прокси {proxy} работает. Ваш IP: {data['origin']}")
                    return True
    except:
        return False
    return False


@app.get("/")
async def root():
    return FileResponse("./templates/index.html")


@app.get("/api/v1.0/heatmap")
async def api_heatmap_v1_0(
    leftdown: str, rightupper: str, width: int, height: int
):
    width, height = int(width), int(height)

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

    map_dowloader = DoubleGisMapDownloader(
        leftdown=leftdown, rightupper=rightupper, width=width, height=height)

    weather_matrix = WeatherMatrix(leftdown, rightupper, width, height)
    weather_request_task = asyncio.create_task(
        weather_matrix.request_weather(STEP_LAT, STEP_LON))

    filepath = f"{IMAGES_PATH}/{generate_random_name(count=32)}.jpg"
    download_task = asyncio.create_task(map_dowloader.download_map(filepath))

    try:
        await download_task
    except MapDownloaderErrorNotEnoughData as e:
        return JSONResponse(
            {"message": "Loader Enough Data"},
            status_code=status.HTTP_502_BAD_GATEWAY,
        )
    except MapDownloaderErrorWhileDownloading as e:
        return JSONResponse(
            {"message": "Something Went Wrong"},
            status_code=status.HTTP_502_BAD_GATEWAY,
        )
    except asyncio.TimeoutError as e:
        print(e)
        if os.path.exists(filepath):
            return JSONResponse(
                {"message": "Error, reached timeout load map"},
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        
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
    try:
        heatmap = HeatMap(filepath, weather_data)
    except HeatmapFileNotFoundException as e:
        print(e.message)
        print(filepath)
        return JSONResponse(
            {"message": "Internal server error, no file to heatmap"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except HeatmapErrImageException as e:
        print(e)
        print(filepath)
        return JSONResponse(
            {"message": "Internal server error, corrupt map image"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except HetmapDataEmptyException as e:
        print(e)
        return JSONResponse(
            {"message": "Internal server error, weather data corrupted"}
        )
    heatmap.get_heatmap()

    return FileResponse(
        filepath,
        status_code=status.HTTP_200_OK,
        headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        },
    )

    # return JSONResponse(
    #     {"message": "Something Went Wrong"},
    #     status_code=status.HTTP_502_BAD_GATEWAY,
    # )
