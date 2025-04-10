import os
import cv2
import numpy as np

# Configuration
IMAGES_DIR = 'images'
MODEL_SAVE_PATH = 'face_model.yml'
FACE_SIZE = (100, 100)  # Resize faces to this size for consistency

def train_face_recognition_model():
    # Initialize face detector and recognizer
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Prepare training data
    faces = []
    labels = []
    label_ids = {}
    current_label = 0

    # Loop through each person's folder
    for person_name in os.listdir(IMAGES_DIR):
        person_dir = os.path.join(IMAGES_DIR, person_name)
        
        if not os.path.isdir(person_dir):
            continue

        label_ids[current_label] = person_name
        print(f"Processing {person_name}...")

        # Process each image in the folder
        for image_file in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_file)
            
            # Read and convert to grayscale
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            detected_faces = face_detector.detectMultiScale(
                gray, 
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            # Use only images with exactly one face
            if len(detected_faces) != 1:
                print(f"Skipping {image_file} - detected {len(detected_faces)} faces")
                continue

            # Crop and resize face
            (x, y, w, h) = detected_faces[0]
            face_roi = gray[y:y+h, x:x+w]
            resized_face = cv2.resize(face_roi, FACE_SIZE)
            
            # Add to training data
            faces.append(resized_face)
            labels.append(current_label)

        current_label += 1

    # Check if we have enough training data
    if len(faces) == 0:
        raise Exception("No valid training data found!")

    # Train the model
    recognizer.train(faces, np.array(labels))
    
    # Save the model and label mapping
    recognizer.save(MODEL_SAVE_PATH)
    np.save('label_mapping.npy', label_ids)
    
    print(f"Training complete. Model saved to {MODEL_SAVE_PATH}")
    print(f"Number of individuals: {len(label_ids)}")
    print(f"Total training faces: {len(faces)}")

if __name__ == '__main__':
    train_face_recognition_model()
    
    
def recognize_face(image_path):
    # Load resources
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_SAVE_PATH)
    label_ids = np.load('label_mapping.npy', allow_pickle=True).item()

    # Process image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect face
    faces = face_detector.detectMultiScale(gray, 1.1, 5)
    if len(faces) != 1:
        return "No face detected" if len(faces) == 0 else "Multiple faces detected"
    
    (x, y, w, h) = faces[0]
    face_roi = cv2.resize(gray[y:y+h, x:x+w], FACE_SIZE)
    
    # Predict
    label, confidence = recognizer.predict(face_roi)
    return label_ids[label]
