import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import os

gesture_label = input("Enter gesture label: ").strip()  
data = []
file_path = 'gesture_data.csv'

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
print("'s' to save , 'q' to quit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            cv2.putText(image, gesture_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            key = cv2.waitKey(1)
            if key == ord('s'):
                if len(landmarks) == 63:  
                    data.append(landmarks + [gesture_label])
                    print(f"Saved sample for '{gesture_label}' — Total: {len(data)}")
                else:
                    print("Incomplete landmark data — skipping")

    
    cv2.imshow('Hand Gesture Capture', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

if data:
    df = pd.DataFrame(data)

    
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
        print(f"Appended {len(data)} samples to existing {file_path}")
    else:
        df.to_csv(file_path, index=False)
        print(f"Created new {file_path} with {len(data)} samples")
else:
    print("No data collected.")
