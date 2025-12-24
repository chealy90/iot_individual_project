import adafruit_dht
import digitalio
from pubnub_client import publish_msg
import time
import datetime


#IO Pins
from board import D2, D3 #GPIO PINS

MIN_TEMP = 20


def flash_led(led):
    for i in range(3):
        led.value = True
        time.sleep(0.2)
        led.value = False
        time.sleep(0.2)
        

try:
    dht_device = adafruit_dht.DHT22(D2, use_pulseio=False)
    led_light = digitalio.DigitalInOut(D3)
    led_light.direction = digitalio.Direction.OUTPUT
    

    while True:
        try:
            temperature = dht_device.temperature
            curr_time = datetime.datetime.now()
            msg = f"{curr_time} Temp: {temperature} ° C"
            print(msg)
            publish_msg(msg)

            #LED
            if temperature < MIN_TEMP:
                flash_led(led_light)
            time.sleep(3)
        except Exception as e:
            print("Error reading temperature: ", e)

except:
    print("Error setting up device")