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

template_list = [1, 2, 3]


async def collab_update_handler(id):
  print(redis_url)
  r = redis.Redis.from_url(redis_url, decode_responses=True)
  collab_list = r.lrange("bitrix24_collabs", 0, -1)
  print(collab_list)
  async with httpx.AsyncClient() as client:
    collab_data = await get_collab_data(client, id)
    print(collab_data["TYPE"] == "collab", collab_data["ORDINARY_MEMBERS"], id not in collab_list)
    if collab_data["TYPE"] == "collab" and collab_data["ORDINARY_MEMBERS"] and id not in collab_list:
      users = await get_users(client)
      extranet_users = [user for user in users if user["ID"] in collab_data["MEMBERS"]]
      if extranet_users:
        crm_object_id = await create_crm_object(client)
        await create_tasks(client, id, crm_object_id, collab_data["OWNER_ID"], extranet_users[0]["ID"], template_list)
        r.rpush("bitrix24_collabs", id)
  
#Получить данные коллаборации по id
async def get_collab_data(client, id):
  url = bitrix24_url + "socialnetwork.api.workgroup.get"
  body = {"params": {"groupId": id} }
  response = await client.post(url, json=body)
  response = response.json()
  return response["result"]
  
#def check_users(collab_user_list, user_list):
  
async def get_users(client):
  url = bitrix24_url + "user.get"
  body = {
    "filter": {
      "user_type": "extranet"
    }
  }
  response = await client.post(url, json=body)
  response = response.json()
  return response["result"]
  
#Создать объект CRM
async def create_crm_object(client):
  url = bitrix24_url + "crm.item.add"
  body = {
    "entityTypeId": 2,
    "fields": {
      
    } 
  }
  response = await client.post(url, json=body)
  response = response.json()
  return response["result"]["ID"]

async def create_tasks(client, group_id, crm_object_id, creator_id, responsible_id, template_list):
  task_list = []
  for template_id in template_list:
    task_id = await create_task(client, group_id, crm_object_id, creator_id, responsible_id, template_id)
    task_list.append(task_if)
  for i in range(0, len(task_list), 2):
    await create_task_connection(client, task_list[i - 1], task_list[i])

#Создать задачу
async def create_task(client, group_id, crm_object_id, creator_id, responsible_id, template_id):
  url = bitrix24_url + "tasks.task.add"
  body = {
    "fields": {
      "createdBy": creator_id,
      "responsibleId": responsible_id, 
      "groupId": group_id,
      "UF_AUTO_710940755509": crm_object_id,
      "forkedByTemplateId": template_id
    } 
  }
  response = await client.post(url, json=body)
  response = response.json()
  return response["result"]

async def create_task_connection(client, task_id_from, task_id_to):
  url = bitrix24_url + "task.dependence.add"
  body = {
    "taskIdFrom": task_id_from,
    "taskIdTo": task_id_to,
    "linkType": 3
  }
  response = await client.post(url, json=body)
  response = response.json()
  return response["result"]
#async def batch_create_tasks(client, task_list):
  
#Изменить стадию обьекта CRM по выполнении задачи
async def update_crm_object_stage(client, id, stage):
  url = bitrix24_url + "crm.item.update"
  body = {"entityTypeId": 2, "id": id, "fields": {"stageId": stage} }
  response = await client.post(url, json=body)
  response = response.json()
  return response["result"]
