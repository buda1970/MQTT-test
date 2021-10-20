from machine import Pin
import time

p2 = Pin(2, Pin.OUT)
p2.on()
count = 0
while(1):
    count += 1
    p2.on()
    time.sleep_ms(500)
    p2.off()
    time.sleep_ms(500)
    print(count)
