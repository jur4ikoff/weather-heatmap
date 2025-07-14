from fastapi import FastAPI, Body, status, APIRouter, Request
from fastapi.responses import FileResponse, Response, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import random

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")

# router = APIRouter(prefix="/pages", tags=["Frontend"])
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root():
    return FileResponse("./templates/index.html")
    # return JSONResponse(content={"message": "Hello World"})


@app.get("/heatmap", response_class=HTMLResponse)
async def get_heatmap(request: Request):
    image_number = random.randint(1, 3)
    image_path = f"/static/images/{image_number}.png"
    return templates.TemplateResponse(
        name="heatmap.html", context={"request": request, "image_path": image_path}
    )


@app.get("/api/heatmap")
async def api_heatmap():
    image_number = random.randint(1, 3)
    image_path = f"/static/images/{image_number}.png"

    return FileResponse(image_path)
