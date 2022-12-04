import machine
import dht
import utime
import ubinascii
from umqttsimple import MQTTClient
import ujson

DHT_sensor = dht.DHT22(machine.Pin(15))

'''MQTT'''
mqtt_server = '192.168.1.101'
client_id = ubinascii.hexlify(machine.unique_id()) # create a random client_id
topic_sub = 'server' # your desired topic for subs
topic_pub = 'DHT_sensor' # your desired topic for pubs

last_message = 0 # for calculate last time of interval
message_interval = 10 # in seconds using time.time()


def sub_cb(topic, msg):
    if topic == b'server' and len(msg) > 0:
        print(f"from server: {msg}");
        
def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    utime.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()


def run():
    global last_message, message_interval
    while True:
        try:
            client.check_msg()
            if (utime.time() - last_message) > message_interval:
                DHT_sensor.measure()
                temp = DHT_sensor.temperature()
                hum = DHT_sensor.humidity()
                temp_f = temp * (9/5) + 32.0
                ujson_msg = {
                    "temp_c": temp,
                    "temp_f": temp_f,
                    "humidity": hum
                }
                msg_string = ujson.dumps(ujson_msg)
                client.publish(topic_pub, msg_string)
                last_message = utime.time()
        except OSError as e:
            print('Failed to read sensor. reconnecting')
            restart_and_reconnect()
            
run()

