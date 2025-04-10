import time
import serial

import adafruit_fingerprint
from main_test import display_oled, clear_display

# If using with Linux/Raspberry Pi and hardware UART:
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    clear_display()
    print("Verify your fingerprint...") # display
    display_oled("Verify your \n fingerprint...")
    time.sleep(1)
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    clear_display()
    print("Searching...") # display
    display_oled("Searching..")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True
    
    
def get_fingerprint_result():
	if get_fingerprint():
		clear_display()
		print("Detected #", finger.finger_id, "with confidence", finger.confidence) #display
		display_oled(f"Detected # {finger.finger_id}")
	else:
		clear_display()
		print("Finger not found") # display
		display_oled("Finger not found")
		
