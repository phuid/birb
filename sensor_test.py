from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
i2c.scan()

import ds1307
from DHT22 import DHT22

ds = ds1307.DS1307(i2c)

dht22 = DHT22(Pin(2,Pin.IN,Pin.PULL_UP),dht11=False)


print("rtc: ", ds.datetime())
print("dht: ", dht22.read())
