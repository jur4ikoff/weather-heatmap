from fastapi import FastAPI, Body, status, APIRouter, Request, Query
from fastapi.responses import FileResponse, Response, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.geo import Geo


import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

# router = APIRouter(prefix="/pages", tags=["Frontend"])
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return FileResponse("./templates/index.html")


@app.get("/api/heatmap")
async def api_heatmap(latitude: str, longitude: str):
    print(latitude, longitude)
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


@app.get("/heatmap", response_class=HTMLResponse)
async def get_heatmap(request: Request):
    image_number = random.randint(1, 3)
    image_path = f"/static/images/{image_number}.png"
    return templates.TemplateResponse(
        name="heatmap.html", context={"request": request, "image_path": image_path}
    )
