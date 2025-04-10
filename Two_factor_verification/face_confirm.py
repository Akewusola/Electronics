import os
import time
import cv2
import numpy as np
from main_test import display_oled, clear_display

# Get face to be confirmed directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, "test_images")
images = sorted(os.listdir(images_dir))
image_name = images[-1]
image_path = os.path.join(images_dir, image_name)

# Configuration
MODEL_PATH = 'face_model.yml'
LABEL_MAPPING = 'label_mapping.npy'
FACE_SIZE = (100, 100)  # Must match training size
CONFIDENCE_THRESHOLD = 100  # Lower is better (0 = perfect match)

def recognize_face(image_path, output_image='result.jpg'):
    # Load resources
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer.read(MODEL_PATH)
    label_mapping = np.load(LABEL_MAPPING, allow_pickle=True).item()

    # Read input image
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not read image")
        clear_display()
        display_oled("Error:\n Could not\n read image")
        return
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    if len(faces) == 0:
        print("No faces detected")
        clear_display()
        display_oled("No faces\n detected")
        time.sleep(1)
        clear_display()
        display_oled("Unknown User!!")
        time.sleep(3)
        return
    
    # Process each detected face
    results = []
    for (x, y, w, h) in faces:
        # Prepare face for recognition
        face_roi = gray[y:y+h, x:x+w]
        resized_face = cv2.resize(face_roi, FACE_SIZE)
        
        # Perform prediction
        label, confidence = recognizer.predict(resized_face)
        
        # Get identity and confidence
        #name = label_mapping.get(label)
        if confidence < CONFIDENCE_THRESHOLD:
            name = label_mapping.get(label, "Unknown")
        else:
            name = "Unknown"
        
        # Store results
        results.append({
            'name': name,
            'confidence': confidence,
            'position': (x, y, w, h)
        })
        
        # Draw rectangle and text
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
        text = f"{name} ({confidence:.1f})"
        cv2.putText(img, text, (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Save and display result
    cv2.imwrite(output_image, img)
    print(f"Result saved to {output_image}")
    
    # Print results to console
    print("\nRecognition Results:")
    for i, result in enumerate(results, 1):
        print(f"Face {i}:")
        print(f"  Hello {result['name']}") # display
        print(f"  Confidence: {result['confidence']:.1f}")
        print(f"  Position: {result['position']}\n")
        
    clear_display()
    display_oled(f"Name: {name}")
    time.sleep(5)
    return results

recognize_face(image_path)
