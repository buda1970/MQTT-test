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
client_id = ubinascii.hexlify(machine.unique_id())
#client = MQTTClient(client_id, mqtt_server, keepalive = 5)
client = MQTTClient(client_id, mqtt_server, user = "test", password = "test", keepalive = 5)
topic_pub = b'sensores/boton'
p2 = Pin(2, Pin.OUT)
p4 = Pin(4, Pin.IN, Pin.PULL_UP)
station = network.WLAN(network.STA_IF)

def conectar_wifi():
  last_message = 0
  message_interval = 5
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Connection successful')

def conectar_mqtt():
  try:
    client.connect()
    return True
  except:
    return False

def desconectar_mqtt():
  client.disconnect()

def publicar_mqtt(count):
  try:
    payload = "{Presionado = " + str(count) + "}"
    print(payload)
    client.publish(topic_pub, payload, qos = 1)
    print('Connected to %s MQTT broker' % (mqtt_server))
    return True
  except:
    return False

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def main():
    print("publicador de mensaje")
    if not station.isconnected():
      conectar_wifi()
    else:
      print("wlan ya esta conectado")
    
    count = 1
    while True:
      p2.on()
      time.sleep_ms(100)
      p2.off()
      
      if conectar_mqtt():
        publicar_mqtt(count)
        count += 1
        desconectar_mqtt()
      else:
        print('Error al conectar MQTT broker')
        time.sleep(10)
      
      
if __name__ == '__main__':
  main()

