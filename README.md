# Hand Gesture Controlled Arduino Car

A webcam-based robotic car controlled through hand gestures. The project combines computer vision, Python, Arduino Uno and an L298N motor driver to control two DC motors.

## Overview

The system uses a laptop webcam to detect hand gestures. MediaPipe identifies hand landmarks, Python counts raised fingers, and commands are transmitted to an Arduino Uno through USB serial communication.

The Arduino interprets these commands and controls the motors through an L298N dual H-bridge motor driver.

## How It Works

1. The webcam captures live video.
2. OpenCV processes the camera frames.
3. MediaPipe detects the hand and identifies its landmarks.
4. Python counts the raised fingers.
5. A corresponding command is sent to the Arduino.
6. The Arduino controls the motors through the L298N driver.

## Gesture Controls

| Hand Gesture | Finger Count | Command | Movement |
|---|---:|---|---|
| Closed fist | 0 | F | Forward |
| One finger | 1 | B | Backward |
| Two fingers | 2 | L | Left |
| Three fingers | 3 | R | Right |
| Four fingers / open palm | 4 | S | Stop |
| No hand detected | — | S | Stop |

## Hardware Components

- Arduino Uno
- L298N dual H-bridge motor driver
- Two DC geared motors
- Two 3.7 V rechargeable batteries connected in series
- Laptop with webcam
- USB cable
- Robot chassis and connecting wires

## Circuit Connections

### Arduino to L298N

| Arduino Pin | L298N Pin |
|---|---|
| D8 | IN1 |
| D9 | IN2 |
| D10 (PWM) | ENA |
| D4 | IN3 |
| D5 | IN4 |
| D3 (PWM) | ENB |
| GND | GND |

### Motors and Power

- Motor 1: OUT1 and OUT2
- Motor 2: OUT3 and OUT4
- Battery positive: L298N motor supply input
- Battery negative: L298N GND

**Important:** Remove the ENA and ENB jumpers when using PWM control. Connect Arduino GND and L298N GND together. Never connect the 7.4 V motor battery directly to the Arduino 5 V pin.

## Software Requirements

- Python 3.12
- OpenCV
- MediaPipe
- PySerial
- Arduino IDE

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd hand-gesture-arduino-car
```

### 2. Install Python dependencies

```bash
py -3.12 -m pip install -r requirements.txt
```

### 3. Upload the Arduino code

1. Open `arduino/hand_gesture_car.ino` in Arduino IDE.
2. Select Arduino Uno as the board.
3. Select the correct COM port.
4. Upload the sketch.

### 4. Configure the serial port

Open `python/hand_control.py` and update the serial port:

```python
SERIAL_PORT = "COM5"
```

Replace COM5 with the port assigned to your Arduino.

### 5. Run the program

```bash
py -3.12 python/hand_control.py
```

The webcam window will display the detected hand and corresponding command.

Press Q to exit.

## Safety and Limitations

- Test with the wheels raised off the ground initially.
- Keep a way to disconnect motor power quickly.
- Gesture recognition depends on lighting, camera angle and hand visibility.
- The current implementation stops the motors when no hand is detected or the program exits normally.
- A hardware emergency stop and Arduino-side serial timeout are not yet implemented.

## Future Improvements

- Gesture stabilisation to reduce accidental movements.
- Arduino-side communication timeout for safer stopping.
- Adjustable motor speed.
- Improved hand-orientation detection.
- Physical emergency-stop switch.
- Additional gestures for more movement controls.

## Technologies Used

Python · OpenCV · MediaPipe · PySerial · Arduino Uno · L298N Motor Driver · C++
