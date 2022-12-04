import machine
import dht
import utime
DHT_sensor = dht.DHT22(machine.Pin(15))

i = 1
while i < 10:
    utime.sleep(5)
    try:
        DHT_sensor.measure()
        temp = DHT_sensor.temperature()
        hum = DHT_sensor.humidity()
        temp_f = temp * (9/5) + 32.0
        print(f"Temperature: {temp} C")
        print(f"Temperature: {temp_f} F")
        print(f"Humidity: {hum} %")
    except OSError as e:
        print(f"Error: {e}")