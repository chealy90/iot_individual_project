import adafruit_dht
import time

#IO Pins
from board import D2 #GPIO 2



try:
    dht_device = adafruit_dht.DHT22(D2, use_pulseio=False)
    

    while True:
        try:
            temperature = dht_device.temperature
            print(f"Temp: ${temperature} ° C")
            time.sleep(3)
        except Exception as e:
            print("Error reading temperature: ", e)

except:
    print("Error setting up device")