from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
i2c.scan()

import ds1307

ds = ds1307.DS1307(i2c)

print("prev", ds.datetime())
now = time.gmtime()
print("time.", now[0], now[1], now[2], now[6], now[3], now[4], now[5], 0)
ds.datetime((now[0], now[1], now[2], now[6], now[3], now[4], now[5], 0));
while (True):
    print("aft", ds.datetime())
    time.sleep_ms(500)
#print(ds.halt(True))
