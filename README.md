# iot_individual_project

## Project idea:
Fridge / freezer temperature sensor /  alert.
Temperature sensor inside fridge, connected to raspberry pi outside of fridge. 
**Pi needs to be outside of fridge/freezer to prevent damage/corrosion**.
Pi sends info to pubnub every two minutes(?), which sends to AWS server. If this outside the allowed range then a warning alert is sent to the user, and the sensor on the pi beeps/light flashes.

The user site allows the user to see their sensors readings history, configure max and minumum temperatures, and name devices.
<img width="1600" height="811" alt="image" src="https://github.com/user-attachments/assets/3f134266-8902-444c-a983-516459265ee7" />






DS18B20 would work best, DHT22 is fine for fridges

