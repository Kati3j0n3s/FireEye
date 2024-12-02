import RPi.GPIO as GPIO
import time

# Gets a single temp data value
def read_temp(sensor_id):
    sensor_file = f'/sys/bus/w1/devices/{sensor_id}/w1_slave'
    with open(sensor_file, 'r') as f:
        lines = f.readlines()
        
    if "YES" in lines[0]:
        temp_string = lines[1].split("t=")[-1]
        celcius_temp = float(temp_string) / 1000.0
        fahrenheit_temp = celcius_temp * 9.0 / 5.0 + 32
        return round (fahrenheit_temp, 2)
    else:
        raise RuntimeError("Failed to read temperature data from DS18b20 sensor.")

# Gets a single altitude data value
def read_alt(barometer_sensor):
	try:
		return barometer_sensor.read_altitude()
	except Exception as e:
		raise RuntimeError(f"Failed to read altitude data: {e}")

# Gets a single pressure data value
def read_pre(barometer_sensor):
	try:
		return barometer_sensor.read_pressure()
	except Exception as e:
		raise RuntimeError(f"Failed to read pressure data: {e}")

# Gets a single humidity data value
def read_hum(HumPin):
	MAX_UNCHANGE_COUNT = 100
	STATE_INIT_PULL_DOWN = 1
	STATE_INIT_PULL_UP = 2
	STATE_DATA_FIRST_PULL_DOWN = 3
	STATE_DATA_PULL_UP = 4
	STATE_DATA_PULL_DOWN = 5
	
	GPIO.setup(HumPin, GPIO.OUT)
	GPIO.output(HumPin, GPIO.HIGH)
	time.sleep(0.05)
	GPIO.output(HumPin, GPIO.LOW)
	time.sleep(0.02)
	GPIO.setup(HumPin, GPIO.IN, GPIO.PUD_UP)
	
	unchanged_count = 0
	last = -1
	data = []
	
	while True:
		current = GPIO.input(HumPin)
		data.append(current)
		if last != current:
			unchanged_count = 0
			last = current
		else:
			unchanged_count += 1
			if unchanged_count > MAX_UNCHANGE_COUNT:
				break
				
	state = STATE_INIT_PULL_DOWN
	lengths = []
	current_length = 0
	
	for current in data:
		current_length += 1
		if state == STATE_INIT_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_INIT_PULL_UP
			continue
		if state == STATE_INIT_PULL_UP:
			if current == GPIO.HIGH:
				state = STATE_DATA_FIRST_PULL_DOWN
			continue
		if state == STATE_INIT_PULL_UP:
			if current == GPIO.HIGH:
				state = STATE_DATA_FIRST_PULL_DOWN
			continue
		if state == STATE_DATA_FIRST_PULL_DOWN:
			if current == GPIO.LOW:
				state = STATE_DATA_PULL_UP
			continue
		if state == STATE_DATA_PULL_UP:
			if current == GPIO.HIGH:
				current_length = 0
				state = STATE_DATA_PULL_DOWN
			continue
		if state == STATE_DATA_PULL_DOWN:
			if current == GPIO.LOW:
				lengths.append(current_length)
				state = STATE_DATA_PULL_UP
			continue
			
	if len(lengths) != 40:
		GPIO.cleanup()
		return None
		
	shortest_pull_up = min(lengths)
	longest_pull_up = max(lengths)
	halfway = (longest_pull_up + shortest_pull_up) / 2
	bits = []
	the_bytes = []
	byte = 0
	
	for lengths in lengths:
		bit = 0
		if length > halfway:
			bit = 1
		bits.append(bit)
	for i in range(0, len(bits)):
		byte = byte << 1
		if bits[i]:
			byte = byte | 1
		if (i + 1) % 8 == 0:
			the_bytes.append(byte)
			byte = 0
			
	checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
	if the_bytes[4] != checksum:
		GPIO.cleanup()
		return None
		
	GPIO.cleanup()
	return the_bytes[0]
	

	
