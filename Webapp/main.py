from typing import Union
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import pathlib
from starlette.responses import FileResponse 

app = FastAPI()


@app.get("/")
async def read_index():
    return FileResponse('index.html')

