import adafruit_dht
from pubnub_client import publish_msg
import time
import datetime


#IO Pins
from board import D2 #GPIO 2



try:
    dht_device = adafruit_dht.DHT22(D2, use_pulseio=False)
    

    while True:
        try:
            temperature = dht_device.temperature
            curr_time = datetime.datetime.now()
            msg = f"{curr_time} Temp: {temperature} ° C"
            print(msg)
            publish_msg(msg)
            time.sleep(3)
        except Exception as e:
            print("Error reading temperature: ", e)

except:
    print("Error setting up device")