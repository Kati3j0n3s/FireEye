import RPi.GPIO as GPIO
import time
import LED
import ReadData

def mode_select(Btn):
	press_start = None
	mode_selected = False

	# Waiting for button press
	while GPIO.input(Btn) == GPIO.HIGH:
		LED.solid('white')
		pass # Keep going till pressed
		
	# Measuring time of button press
	press_start = time.time()
	
	# Continuously check while button is pressed
	while GPIO.input(Btn) == GPIO.LOW:
		press_duration = time.time() - press_start
		
		if press_duration >= 3 and not mode_selected:
			print("Long hold detected: Drone mode")
			LED.stop()
			mode_selected = True
			return 'drone'
	
	if not mode_selected:
		print("Short press detected: Walk mode")
		LED.stop()
		return 'walk'
		
def drone_mode(barometer_sensor):
	print("DRONE MODE")
	""" Light Indications """
	LED.stop()
	LED.pulse('green')
	
	
	""" Drone Instructions """
	DATA_ALTITUDE_THRESHOLD = 10
	
	starting_alt = ReadData.read_alt(barometer_sensor)
	while True:
		# Checks altitude every 2 seconds
		time.sleep(2)
		current_alt = ReadData.read_alt(barometer_sensor)
		altitude_diff = abs(current_alt - starting_alt)
		
		print(f"Current Altitude: {current_alt} ft. | Difference: {round(altitude_diff, 3)} ft.")
		
		if altitude_diff >= DATA_ALTITUDE_THRESHOLD:
			print(f"Altitude threshold reached: {altitude_diff} ft. Starting data collection.")
			break
	
	collecting_data(conn, barometer_sensor)
	
	
	
def walk_mode():
	print("WALK MODE")
	""" Light Indications """
	LED.stop()
	LED.solid('green')
	return None
	
