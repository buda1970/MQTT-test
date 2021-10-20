import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
from machine import Pin
esp.osdebug(None)
import gc
gc.collect()

global client_id, mqtt_server
client_id = 'PL'
ssid = 'GatoDumas'
password = 'GatoAnitaKevin!'
mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub_temp = b'casa/sensor'
p2 = Pin(2, Pin.OUT)

def connect_wifi():
    #EXAMPLE IP ADDRESS
    #mqtt_server = '192.168.1.106'
    last_message = 0
    message_interval = 5

    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
      pass

    print('Connection successful')


def connect_mqtt():
    client = MQTTClient(client_id, mqtt_server)
    #client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_server))
    return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def main():
    temp = 1
    connect_wifi()
    connect_mqtt()
    try:
        client = connect_mqtt()
    except OSError as e:
        restart_and_reconnect()

    while True:
        try:
            time.sleep(20)
            print(temp)
            p2.on()
            client.publish(topic_pub_temp, '{ sensor: ' + str(temp) + ' }')
            time.sleep_ms(200)
            p2.off()
            temp += 1
            
        except OSError as e:
            restart_and_reconnect()


if __name__ == '__main__':
    main()
    
sys.exit(0)
