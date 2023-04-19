#dht11
from machine import I2C, Pin
from time import sleep_ms
from DHT22 import DHT22
import picosleep

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
i2c.scan()

import ds1307

ds = ds1307.DS1307(i2c)

dht22 = DHT22(Pin(2,Pin.IN,Pin.PULL_UP),dht11=True)

proximity = Pin(22, Pin.IN, Pin.PULL_UP)
led = Pin(25, Pin.OUT)
download_pin = Pin(5, Pin.IN, Pin.PULL_UP)

wakeup_reason_interrupt = False

def idk(a):
    global wakeup_reason_interrupt
    wakeup_reason_interrupt = 1 + proximity.value()

proximity.irq(idk, Pin.IRQ_FALLING)

counter = 0

if (not download_pin.value()):
    while True:
        sleep_ms(100)
        led.toggle()
while True:
    led.value(0)
    wakeup_reason_interrupt = 0
    picosleep.seconds(3600) #deepsleep

    dhtdata = None
    dsdata = None
    try:
        dhtdata = dht22.read()
    except Exception as e:
        print(e)
    try:
        dsdata = ds.datetime()
    except Exception as e:
        print(e)

    if wakeup_reason_interrupt == 2:
        continue

    f = open("data.csv", "a")
    f.write("{},{},{},{}".format(counter, dhtdata, dsdata, wakeup_reason_interrupt).replace("(", "").replace(")", "").replace(" ", ""))
    #for x in ds.datetime():
    #    f.write("," + str(x))
    f.write("\n")
    f.close()
    #DEBUG print("{},{},{},{}".format(counter, dhtdata, dsdata, wakeup_reason_interrupt).replace("(", "").replace(")", "").replace(" ", ""))
    
    counter += 1
    
    if dsdata == None or dhtdata == (None,None):
        for x in range(10):
            led.value((x+1) % 2)
            sleep_ms(49)
    elif wakeup_reason_interrupt == 1:
            for x in range(4):
                led.value((x+1)%2)
                sleep_ms(200)
    else:
        led.value(1)
        sleep_ms(490)
