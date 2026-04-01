from fastapi import FastAPI, Request
import multipart
import re
from api.functions import new_order_handler, update_orders
#from api.handlers import set_time, update, clear_keys, hash_password
from urllib.parse import unquote, urlparse

app = FastAPI()


@app.get('/api/update')
async def get_handler():
    try:
        result = await update_orders()
        return result 
    except Exception as e:
        print(e)
        return e

@app.post('/api/create')
async def post_handler(request: Request):
    try:
        print(request)
        body = await request.json()
        print(body)
        result = await new_order_handler(body)
        return result
    except Exception as e:
        print(e)
        return e
        
@app.post('/api/webhook')
async def webhook(request: Request):
    ...
        
