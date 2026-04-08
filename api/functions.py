from urllib.parse import unquote
from datetime import datetime, timedelta
import httpx
import re
import math
import numbers
import time
import os
import redis
import secrets
import string
import random 
import hashlib
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.local")
redis_url = os.getenv("REDIS_URL")
bitrix24_url = os.getenv("BITRIX24_URL")

async def collab_update_handler(id):
  r = redis.Redis.from_url(redis_url, decode_responses=True)
  async with httpx.AsyncClient() as client:
    collab_data = await get_collab_data(client, id)
    if collab_data["TYPE"] == "collab" and collab_data["USERS"] > collab_data["MODERATORS"]:
      mapping = {"
      r.hset(f"b24-collab:{id}", mapppin

    order_id = await create_order(client, items, note, data["id"])
    r.set(f"insales-mpfit:{order_id}", "NEW")

#Получить данные коллаборации по id
async def get_collab_data(client, id):
  url = bitrix24_url + "socialnetwork.api.workgroup.get"
  body = {"params": {"groupId": id} }
  response = await client.post(url, json=body)
  response = response.json()
  return response["result"]

#Создать объект CRM

#Создать задачи

#Изменить стадию обьекта CRM по выполнении задачи


async def update_orders():
  r = redis.Redis.from_url(redis_url, decode_responses=True)
  keys = r.keys("insales-mpfit:*")
  values = r.mget(keys)
  cached_orders = {key.replace("insales-mpfit:",""): value for key, value in zip(keys, values)}
  print(cached_orders)
  async with httpx.AsyncClient() as client:
    orders = await get_orders(client, list(cached_orders.keys()), 0)
    for order in orders:
      if order["status"] != cached_orders[order["id"]]:
        await update_order(client, order["number"], order["status"])
        r.set(f"insales-mpfit:{order["id"]}", order["status"])
      
async def check_order_status(client, id):
  ...

async def get_tracking_number(client, redis_client, id):
  try:
    tracking_number = await get_cdek_tracking_number(client, redis_client, id)
    if tracking_number is None:
      tracking_number = await get_pochta_tracking_number(client, redis_client, id)
    return tracking_number
  except Exception as e:
    print(e)
    return None

def check(value):
  return "" if value is None else value
