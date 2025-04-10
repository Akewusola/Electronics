import os
import time
from enroll_fingerprint import enroll_finger
from verify_fingerprint import get_fingerprint_result
from capture import enroll, verify
from main_test import display_oled, clear_display

# Print welcome message
print("Welcome!")  
display_oled("Welcome to our\n verification system!")
time.sleep(1)
clear_display()

while True:
	# Task to be performed
	clear_display()
	display_oled("Enroll User(E)\n Verify User(V):")
	task = input("Enroll User(E)/Verify User(V):")
	clear_display()

	# Get face to be confirmed directory
	script_dir = os.path.dirname(os.path.abspath(__file__))
	users_dir = os.path.join(script_dir, "images")
	users = sorted(os.listdir(users_dir))
	no_of_users = len(users)

	# Functions based on each task
	if task == 'E':
		user = input("Enter user name:") # Get user's name
		user_id = no_of_users + 1 # give unique ID to each user
		print(f"Your ID is {user_id}") # display
		enroll_finger(user_id)  # Enroll user fingerprint
		time.sleep(1)
		
		clear_display()
		display_oled("Get ready for\n facial verification")
		# Take face picture ten times
		i = 1
		while i <= 10:
			enroll(user, user_id)
			if i < 10:
				clear_display()
				print("Get ready to take another picture")
				display_oled("Get ready to take another picture")
			i += 1
		# Train the model
		os.system("python3 t_models.py") # Train the model
		clear_display()
		print("Successfully enrolled!") # display
		display_oled(f"Successfully\n enrolled\n {user}")
		time.sleep(3)
	elif task == 'V':
		get_fingerprint_result() # Getting fingerprint result
		time.sleep(1)
		clear_display()
		display_oled("Preparing for\n facial \n recognition")
		verify() # Take the face picture
		clear_display()
		os.system("python3 face_confirm.py")
	
	
	
	
	
	
