# Diagnostic check to be run initially and when called if
# user calls for it.

def diagnostic_check():
    print("initializing diagnostics...")

    try:
        if GPIO.input(BtnPin) in None:
            print("Diagnostic failed: Button not responding.")
            return False
        if GPIO.input(TempPin) in None:
            print("Diagnostic failed: Temp Sensor not responding.")
            return False
        if GPIO.input(HumidityPin) in None:
            print("Diagnostic failed: Humidity Sensor not responding.")
            return False


    except Exception as e:
        print(f"diagnostic check failed: {e}")




    print("finished diagnostic")
