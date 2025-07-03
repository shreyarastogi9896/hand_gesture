import cv2
import mediapipe as mp
import numpy as np
import serial
from tensorflow.keras.models import load_model
import time


model = load_model("gesture_model.h5")
class_names = np.load("gesture_labels.npy", allow_pickle=True)


bluetooth_port = "COM4"  
baud_rate = 9600
try:
    ser = serial.Serial(bluetooth_port, baud_rate, timeout=1)
    print(f"Connected to {bluetooth_port}")
    time.sleep(2)  
except Exception as e:
    print(f"Error connecting to serial port: {e}")
    ser = None


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils


gesture_to_command = {
    "Forward": "F",
    "Backward": "B",
    "Left": "L",
    "Right": "R",
    "stop": "S"
}


cap = cv2.VideoCapture(0)
last_sent_command = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.flip(frame, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            if len(landmarks) == 63:
                prediction = model.predict(np.array([landmarks]), verbose=0)
                gesture = class_names[np.argmax(prediction)]
                confidence = np.max(prediction)

                cv2.putText(image, f"{gesture} ({confidence:.2f})", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                
                command = gesture_to_command.get(gesture, None)
                if command and command != last_sent_command and ser:
                    ser.write(command.encode())
                    print(f"Sent command: {command} for gesture: {gesture}")
                    last_sent_command = command

    cv2.imshow("Gesture Control", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()
