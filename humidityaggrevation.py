#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

DHTPIN = 17  # Your GPIO pin
GPIO.setmode(GPIO.BCM)

def read_dht11():
    # Initialize the sensor
    GPIO.setup(DHTPIN, GPIO.OUT)
    GPIO.output(DHTPIN, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(DHTPIN, GPIO.LOW)
    time.sleep(0.02)
    GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

    # Read sensor data
    data = []
    for _ in range(40):
        data.append(GPIO.input(DHTPIN))
        time.sleep(0.01)

    # Process the data
    if len(data) != 40:
        print("Failed to read data")
        return None

    humidity = data[0:8]
    temperature = data[16:24]
    print("Humidity Data: ", humidity)
    print("Temperature Data: ", temperature)
    
    return humidity, temperature

def main():
    print("Starting DHT11 Test")
    while True:
        result = read_dht11()
        if result:
            humidity, temperature = result
            print(f"Humidity: {humidity} Temperature: {temperature}")
        time.sleep(2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
