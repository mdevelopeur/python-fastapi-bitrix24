import time


async def obtain_cdek_token(client, redis_client):
  url = "https://api.cdek.ru/v2/oauth/token?grant_type=client_credentials"
  result = await client.post(url=url, auth=(cdek_client, cdek_secret))
  result = result.json()
  timestamp = time.now()
  r.set(f"insales_mpfit_cdek_token:{timestamp}", result["access_token"])
  return result["access_token"]

async def get_cdek_order(client, token, id):
  url = f"https://api.cdek.ru/v2/orders?im_number={id}"
  headers = {"Authorization": f"Bearer {token}"}
  result = await client.get(url=url, headers=headers)
  result = result.json()
  return 
