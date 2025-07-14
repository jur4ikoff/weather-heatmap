from fastapi import FastAPI, Body, status, APIRouter, Request
from fastapi.responses import FileResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

router = APIRouter(prefix="/pages", tags=["Frontend"])
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return JSONResponse(content={"message": "Hello World"})

@app.get("/heatmap")
async def get_heatmap(request: Request):
        return templates.TemplateResponse(name="index.html", context={"request" : request})

@app.get("/api/get_heatmap")
async def api_get_heatmap():
      pass