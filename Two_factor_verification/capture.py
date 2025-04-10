import time
from picamera2 import Picamera2
import os
from datetime import datetime
from main_test import display_oled, clear_display

def enroll(name, passcode):
    # Create user folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'images',name)
    os.makedirs(images_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"image_{timestamp}.jpg"
    file_path = os.path.join(images_dir, filename)

    picam2 = None
    
    clear_display()

    try:
        # Initialize the camera
        picam2 = Picamera2()
        
        # Configure camera settings
        config = picam2.create_still_configuration(main={"size": (1024, 768)})
        picam2.configure(config)
        
        # Start the camera
        picam2.start()
        
        # Warm-up time for the camera
        time.sleep(2)
        
        # Countdown before taking picture
        print("Getting ready to take picture") # display
        display_oled("Getting ready\n to take picture\n in 2 seconds")
        time.sleep(2)
        clear_display()
        print("Taking picture now.....") # display
        
        # Capture image
        picam2.capture_file(file_path)
        print(f"Image saved to: {file_path}")
        display_oled("Image captured")

    except Exception as e:
        clear_display()
        print(f"An error occurred: {str(e)}")
        display_oled(f"An error occurred: {str(e)}")
        

    finally:
        # Ensure camera resources are released
        if picam2 is not None:
            picam2.close()    
            
def verify():
    # Storing image in appropriate directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, 'test_images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"image_{timestamp}.jpg"
    file_path = os.path.join(images_dir, filename)

    picam2 = None

    try:
        # Initialize the camera
        picam2 = Picamera2()
        
        # Configure camera settings
        config = picam2.create_still_configuration(main={"size": (1024, 768)})
        picam2.configure(config)
        
        # Start the camera
        picam2.start()
        
        # Warm-up time for the camera
        time.sleep(2)
        
        # Countdown before taking picture
        clear_display()
        print("Taking picture in 2 seconds...") # display
        display_oled("Taking picture\n in 2 seconds...")
        time.sleep(1)
        for i in range(3, 0, -1):
            print(i) # display
            time.sleep(1)
        
        # Capture image
        picam2.capture_file(file_path)
        print("Image captured") # display
        clear_display()
        display_oled("Image captured")
        print(f"Image saved to: {file_path}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Ensure camera resources are released
        if picam2 is not None:
            picam2.close()
            
    
