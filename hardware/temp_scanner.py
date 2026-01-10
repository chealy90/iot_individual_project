#https://www.geeksforgeeks.org/python/python-async/

import adafruit_dht
import digitalio
from pubnub_client import *
import time
import datetime
import asyncio
import json
from dotenv import load_dotenv
import os
from board import D2, D3, D4, D17


#Load env 
load_dotenv()

'''
D2 - Scanner
D3 - Red LED
D4 - Buzzer
D17 - Green LED

'''

#File I/O methods for temp file
def read_temps_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def write_temps_file(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f)



#scanner values
DEVICE_ID = os.getenv("DEVICE_ID")
initial_temps = read_temps_file("temps.json")
MAX_TEMP = initial_temps["MAX_TEMP"]
MIN_TEMP = initial_temps["MIN_TEMP"]





#subscription
subscription = pubnub.channel(CHANNEL).subscription()
subscription.on_message = lambda message: handle_message(message)
subscription.subscribe()


def handle_message(message):
    global MIN_TEMP, MAX_TEMP
    print(message.message)
    msg = message.message

    if msg.get("message_type") == "update_sensor":
        MAX_TEMP = msg.get("max_temp")
        MIN_TEMP = msg.get("min_temp")

        new_json_data = {
            "MAX_TEMP": MAX_TEMP,
            "MIN_TEMP": MIN_TEMP
        }

        write_temps_file("temps.json", new_json_data)
        







async def flash_led(led):
    for i in range(3):
        led.value = True
        await asyncio.sleep(0.2)
        led.value = False
        await asyncio.sleep(0.2)



async def buzz_alarm(buzzer):  
    for i in range(3):
        for pulse in range(60):
            buzzer.value = True
            await asyncio.sleep(0.001)
            buzzer.value = False
            await asyncio.sleep(0.01)
        await asyncio.sleep(0.02)


async def activate_temp_alarms(buzzer, led):
    await asyncio.gather(buzz_alarm(buzzer), flash_led(led))
        


async def main():
    try:
        dht_device = adafruit_dht.DHT22(D2, use_pulseio=False)

        green_led = digitalio.DigitalInOut(D17)
        green_led.direction = digitalio.Direction.OUTPUT

        red_led = digitalio.DigitalInOut(D3)
        red_led.direction = digitalio.Direction.OUTPUT

        buzzer = digitalio.DigitalInOut(D4)
        buzzer.direction = digitalio.Direction.OUTPUT
        

        while True:
            try:
                temperature = dht_device.temperature
                curr_time = datetime.datetime.now().isoformat()
                msg = f"{curr_time} Temp: {temperature} ° C"
                json_msg = {
                    "time": curr_time,
                    "temperature": temperature,
                    "device_id": DEVICE_ID
                }
                print(json_msg)
                publish_msg(json_msg)
                print(MIN_TEMP)
                print(MAX_TEMP)

                #LED / Buzzer
                if temperature < MIN_TEMP:
                    green_led.value = False
                    await activate_temp_alarms(buzzer, red_led)
                else:
                    green_led.value = True
                await asyncio.sleep(3)
            except Exception as e:
                print("Error reading temperature: ", e)

    except:
        print("Error setting up device")




if __name__ == "__main__":
    asyncio.run(main())