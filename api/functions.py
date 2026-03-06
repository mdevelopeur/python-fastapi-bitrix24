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

async def new_order_handler(data):


async def get_products(client, last_id):
  url = mpfit + ""
  body = {
  "limit": 200,
  "last_id": last_id
  }
  result = await client.post(url=url, headers=mpfit_headers, json=body)
  result = result.json()
  #products = result["data"]
  if len(result["data"]) == 200:
    products = await get_products(client, result["last_id"])
    products.extend(result["data"])
    return products
  else:
    return result["data"]

def get_order_items(items, products):
  output = []
  for item in items:
    product = next((product for product in products if product['article'] == item["sku"]), None)
    if product is not None:
      output.append({"id": product["id"], "quantity": product["quantity"]})

  return output

async def create_order(client, items):
  url = mpfit + ""
  body = {"items": items, "shipment_date": ""}
  result = await client.post(url=url, headers=mpfit_headers, json=body)
  result = result.json()
  return result["order"]["id"]

async def get_orders(client, id_list, last_id):
  url = mpfit + ""
  body = {"limit": 200, "last_id": 0, "filter": {"ids": id_list[:200]}}
  result = await client.post(url=url, headers=mpfit_headers, json=body)
  result = result.json()
  id_list = id_list[200:]
  if id_list:
    orders = await get_orders(client, id_list, result["last_id"])
    orders.extend(result["data"])
    return orders
  else:
    return result["data"]

async def update_order(client, order, status):
  url = f"{insales}{order}.json"
  body = 
  result = await client.post(url=url, headers=mpfit_headers, json=body)
  result = result.json()
  return 

async def update_orders():
  r = redis.Redis.from_url(redis_url, decode_responses=True)
  keys = r.keys("insales-mpfit:*")
  statuses = r.mget(keys)
  id_list = [key.replace("insales-mpfit:","") for key in keys]
  


async def check_order_status(client, id, ):
  
