import time
import sys
import Pi_HDC2080

hdc2000 = Pi_HDC2080.Pi_HDC2080()

while True:
    pressure = bmp280.get_pressure()
    print("temperature : %3.1f, humidity : %3.1f " %
          (hdc2000.readTemperature(), hdc2000.readHumidity()))
    time.sleep(1)
