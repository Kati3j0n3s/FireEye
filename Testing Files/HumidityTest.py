import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 23

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
	print(f'{temperature} {humidity}')
else:
	print('failed')
