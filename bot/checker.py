import json
import os

import aiohttp
from dotenv import load_dotenv
from loguru import logger

env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")


@logger.catch
async def get_services():

    url = "https://api.imeicheck.net/v1/services"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept-Language": "en",
        "Content-Type": "application/json",
    }

    payload = {}

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, headers=headers, data=payload) as response:
            response = await response.json()
    return response


@logger.catch
async def check_device(deviceId, service):

    url = "https://api.imeicheck.net/v1/checks"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept-Language": "en",
        "Content-Type": "application/json",
    }

    payload = json.dumps({"deviceId": deviceId, "serviceId": service})

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.post(url,
                                headers=headers,
                                data=payload) as response:
            response = await response.json()

    result = ""
    for key, value in response.items():
        result += f"{key}: {value}\n"
    return result
