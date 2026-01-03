#https://www.geeksforgeeks.org/python/python-async/

import adafruit_dht
import digitalio
from pubnub_client import publish_msg
import time
import datetime
import asyncio


'''
D2 - Scanner
D3 - Red LED
D4 - Buzzer
D17 - Green LED

'''


#IO Pins
from board import D2, D3, D4, D17 #GPIO PINS

MIN_TEMP = 20


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
                curr_time = datetime.datetime.now()
                msg = f"{curr_time} Temp: {temperature} ° C"
                json_msg = {
                    "time": curr_time,
                    "temperature": temperature

                }
                print(json_msg)
                publish_msg(json_msg)

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