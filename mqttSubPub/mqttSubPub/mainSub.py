import machine
from machine import Pin
from umqttsimple import MQTTClient
import time
import network
import ubinascii

import esp
esp.osdebug(None)
import gc
gc.collect()


global client_id, mqtt_server
client_id = 'PL'
ssid = 'GatoDumas'
password = 'GatoAnitaKevin!'
mqtt_server = '192.168.1.144'
#mqtt_port   = 1883
#client_id = ubinascii.hexlify(machine.unique_id())
client_id = "PL1"
topic_pub = b'sensores/#'
p2 = Pin(2, Pin.OUT)
p4 = Pin(4, Pin.IN, Pin.PULL_UP)
station = network.WLAN(network.STA_IF)

def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"{on}":
        p2.on()
        state = 1
    elif msg == b"{off}":
        p2.off()
        state = 0
    elif msg == b"{blink}":
        blink_led()

def conectar_wifi():
  last_message = 0
  message_interval = 5
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Connection successful')

def blink_led():
    p2.on()
    time.sleep_ms(50)
    p2.off()

def main():
    print("subscritor de mensaje")
    if not station.isconnected():
        conectar_wifi()
    else:
        print("wlan ya esta conectado")
    
    #client = MQTTClient(client_id, mqtt_server, keepalive = 5)
    client = MQTTClient(client_id, mqtt_server, user = "test", password = "test", keepalive = 60)
    client.set_callback(sub_cb)
    client.connect(clean_session = False)
    client.subscribe(topic_pub, qos = 1)
    
    try:
        while True:
            client.wait_msg()
            blink_led()
            
    finally:
        client.disconnect()
        pass

    
if __name__ == '__main__':
  main()
  
