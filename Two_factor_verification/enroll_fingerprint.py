import time
import serial

import adafruit_fingerprint
from main_test import display_oled, clear_display

# If using with Linux/Raspberry Pi and hardware UART:
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="") # display
            clear_display()
            display_oled("Place finger\n on sensor...")
            time.sleep(2)
        else:
            clear_display()
            print("Place same finger again...", end="") # display
            display_oled("Place same\n finger again...")
        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                clear_display()
                print("Image taken") # display
                display_oled("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                clear_display()
                print(".", end="")
                display_oled(".")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                clear_display()
                print("Imaging error")
                display_oled("Imaging error")
                return False
            else:
                clear_display()
                print("Other error")
                display_oled("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            clear_display()
            print("Remove finger")
            display_oled("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        clear_display()
        print("Created")
        display_oled("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            clear_display()
            print("Prints did not match")
            display_oled("Prints did not match")
        else:
            clear_display()
            print("Other error")
            display_oled("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True
