import RPi.GPIO as GPIO
import time
import os
import sys
import LED
import OldFiles.ReadData as ReadData
import OldFiles.Database as Database
import OldFiles.Diagnostic as Diagnostic
from datetime import datetime

def mode_select(Btn1, Btn2, TempPin, HumPin, barometer_sensor, camera):
	press_start = None
	mode_selected = False
	
	while True:
		# Checking if Btn1 - Mode Selection Button is pressed
		if GPIO.input(Btn1) == GPIO.LOW:
			press_start = time.time()
			while GPIO.input(Btn1) == GPIO.LOW:
				press_duration = time.time() - press_start
				
				if press_duration >= 3 and not mode_selected:
					print("Long hold detected: Drone Mode")
					LED.stop()
					mode_selected = True
					return 'drone'
					
			if not mode_selected:
				print("Short press detected: Walk Mode")
				LED.stop()
				return 'walk'
				
		# Checking if Btn2 - Diagnostic or Reboot is pressed
		if GPIO.input(Btn2) == GPIO.LOW:
			print("Second button press")
			press_start = time.time()
			while GPIO.input(Btn2) == GPIO.LOW:
				pass
				
			press_duration = time.time() - press_start
				
			if press_duration >= 1:
				print("Long hold detected: Reboot")
				LED.solid('red')
				# Function to reboot
				#os.system('sudo reboot')
				
				GPIO.cleanup()
				sys.exit()
				
			else:
				print("Short press detected: Diagnostics")
				Diagnostic.diagnostic_check(Btn1, Btn2, TempPin, HumPin, barometer_sensor, camera)
				LED.stop()
				
		LED.solid('white')
		time.sleep(0.1)
		
def drone_mode(conn, barometer_sensor, camera):
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
			
	# Simulated Full Flight Collection - NEED TO MODIFY FOR ACTUAL FLIGHT LATER!!!!
	flight_start_time = datetime.now()
	
	# Getting flight_id from first call
	flight_id = Database.collect_flight_data(conn, barometer_sensor, camera, interval=20, i = 0)

	for i in range(1, 3):
		Database.collect_flight_data(conn, barometer_sensor, camera, interval=20, i = i)
		
	flight_end_time = datetime.now()
	flight_duration = (flight_end_time - flight_start_time).total_seconds()
	
	Database.complete_flight(conn, flight_id, flight_end_time)
	
	LED.stop()
	print("Flight data collection complete!")

	
def walk_btn(Btn):
	# Waiting for button press
	while GPIO.input(Btn) == GPIO.HIGH:
		pass
		
	# Measuring how long button pressed
	press_start = time.time()
	while GPIO.input(Btn) == GPIO.LOW:
		pass
		
	press_duration = time.time() - press_start
	
	if 0 < press_duration < 1:
		print("short press, collecting data.")
		return 'short'
	elif press_duration > 1:
		print("long press, returning to mode selection.")
		return 'long'

	return None
	
	
def walk_mode(Btn, conn, barometer_sensor, camera):
	print("WALK MODE")
	
	while True:
		LED.stop()
		LED.solid('green')
		
		press_type = walk_btn(Btn)
		if press_type == 'short':
			print("Collecting Data.")
			Database.collect_walk_data(conn, barometer_sensor, camera)
		elif press_type == 'long':
			print("Exit Walk Mode")
			LED.stop()
			return
		else:
			print("invalid")
	
