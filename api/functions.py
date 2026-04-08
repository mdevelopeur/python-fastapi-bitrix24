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

"""Компания работает по франчайзинговой модели. После продажи франшизы партнер передается в Отдел запуска для сопровождения до открытия точки.
Каждый партнер ведется как отдельный проект, реализуемый через Коллабу Bitrix24.
В коллабе участвуют менеджер запуска и партнер (гость системы). Все задачи по проекту выполняет партнер своими силами, менеджер ставит задачи, консультирует и контролирует выполнение.
Необходимо автоматизировать данный процесс.
Основная логика:
Создание проекта
При создании новой коллабы и добавлении партнера автоматически создается проект запуска и стартовый набор задач.
Назначение задач
Все задачи внутри коллабы автоматически назначаются исполнителю партнеру (гость Bitrix24). Менеджер выступает постановщиком и контролером задач.
Задачи должны открываться поэтапно. После выполнения текущей задачи автоматически создается или открывается следующая задача проекта.
Связь с CRM
Каждый проект должен параллельно отображаться в CRM как отдельный объект, проходящий по этапам запуска (например: поиск помещения → договор аренды → ремонт → подготовка открытия → открытие).
Переход между этапами CRM должен происходить автоматически на основе выполнения ключевых задач проекта.
Два уровня контроля
Руководитель — видит все проекты и их текущий этап через CRM.
Менеджер — работает через задачи проекта и контролирует выполнение партнером.
Цель внедрения — систематизировать запуск франшизных точек, минимизировать ручные действия и обеспечить прозрачный контроль проектов. 
"""

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


async def get_collab_data(client, id):
  url = bitrix24_url + "socialnetwork.api.workgroup.get"
  body = {"params": {"groupId": id} }
  response = await client.post(url, json=body)
  response = response.json()
  return response["result"]



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
