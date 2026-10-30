import cv2
import mediapipe as mp
import serial
import time

# Change COM3 to your Arduino's actual port
arduino = serial.Serial("COM5", 9600, timeout=1)
time.sleep(2)

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

last_command = None

def count_fingers(hand):
    landmarks = hand.landmark
    tips = [8, 12, 16, 20]
    joints = [6, 10, 14, 18]

    return sum(
        landmarks[tip].y < landmarks[joint].y
        for tip, joint in zip(tips, joints)
    )

def gesture_to_command(fingers):
    if fingers == 0:
        return "F"
    elif fingers == 1:
        return "B"
    elif fingers == 2:
        return "L"
    elif fingers == 3:
        return "R"
    else:
        return "S"

try:
    while True:
        success, frame = camera.read()

        if not success:
            print("Could not access webcam.")
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        command = "S"
        display_text = "No hand detected - STOP"

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            fingers = count_fingers(hand)
            command = gesture_to_command(fingers)

            display_text = f"Fingers: {fingers} | Command: {command}"
            mp_draw.draw_landmarks(
                frame, hand, mp_hands.HAND_CONNECTIONS
            )

        if command != last_command:
            arduino.write(command.encode())
            last_command = command

        cv2.putText(
            frame, display_text, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
        )

        cv2.imshow("Arduino Hand Control", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    if arduino.is_open:
        arduino.write(b"S")
        arduino.close()

    camera.release()
    cv2.destroyAllWindows()
    hands.close()