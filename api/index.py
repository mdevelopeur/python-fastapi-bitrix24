from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
import multipart
import re

#from api.handlers import set_time, update, clear_keys, hash_password
from urllib.parse import unquote, urlparse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get('/api/update')
async def get_handler():
    try:
        result = await update_orders()
        return result 
    except Exception as e:
        print(e)
        return e

@app.post('/api/post')
async def post_handler(request: Request):
    try:
        body = await request.body()
        print(unquote(body))
        body = await request.json()
        print(body)
        result = await new_order_handler(body)
        return result
    except Exception as e:
        print(e)
        return e
        
@app.get('/api/index', response_class=HTMLResponse)
async def read_index():
    return FileResponse('templates/index.html')
