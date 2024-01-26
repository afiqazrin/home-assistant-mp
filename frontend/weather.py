import python_weather
from datetime import datetime
import asyncio
import os

import requests


def get_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()["ip"]
        else:
            print(response.status_code)
            return None
    except requests.RequestException as e:
        # print(response.status_code)
        return None


def get_location():
    try:
        ip_address = get_ip()
        response = requests.get(f'https://ipapi.co/{ip_address}/json/')
        if response.status_code == 200:
            location_data = response.json().get("city")
            return location_data
        else:
            print(response.status_code)
            return None
    except requests.RequestException as e:
        # print(response.status_code)
        return None

async def getweather(location):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        try:
            weather = await client.get(location)
            tempf = weather.current.temperature
            desc = weather.current.description
            humid=weather.current.humidity
            return tempf, desc, humid
        except Exception as e:
            print(f"Error getting weather data: {e}")
            return None, None, None  # or handle the error as per your application's logic

async def dashboardsent():
    global tempc, desc, humid
    while True:
        #   asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
          townname=get_location()
          if townname==None or townname=='':
            townname='Singapore'
          else:
            townname=townname
        


          tempf, desc, humid = await getweather(townname)
          tempc = format((tempf - 32) * 5/9, '.2f')
          return tempc, desc, humid
