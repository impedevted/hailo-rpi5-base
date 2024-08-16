import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

import threading

import tkinter as tk

# Create the I2C bus interface
i2c = busio.I2C(SCL, SDA)

# Create a PCA9685 object
pca = PCA9685(i2c)
pca.frequency = 50  # Set frequency to 60 Hz for motor control

# Define the channels used for the motors
MOTOR1_IN1 = 0
MOTOR1_IN2 = 1
MOTOR2_IN1 = 2
MOTOR2_IN2 = 3
MOTOR3_IN1 = 6
MOTOR3_IN2 = 7
MOTOR4_IN1 = 8
MOTOR4_IN2 = 9

ENA_CHANNEL_1 = 4
ENB_CHANNEL_1 = 5
ENA_CHANNEL_2 = 10
ENB_CHANNEL_2 = 11

# Define the channels for the servos (robot arm)
SERVO1_CHANNEL = 12
SERVO2_CHANNEL = 13
SERVO3_CHANNEL = 14
SERVO4_CHANNEL = 15


def set_servo_angle(channel, target_angle):
    min_pulse = 0.7  # Adjust if needed
    max_pulse = 2.75  # Adjust if needed

    pulse_length = min_pulse + (target_angle / 180.0) * (max_pulse - min_pulse)
    duty_cycle = int((pulse_length / 20.0) * 0xFFFF)
    pca.channels[channel].duty_cycle = duty_cycle

def set_motor(channel1, channel2, speed):
    """Set motor speed.
    speed: -1.0 to 1.0 where -1.0 is full speed reverse, 0 is stop, and 1.0 is full speed forward
    """
    if speed > 0:
        # Forward
        pca.channels[channel1].duty_cycle = int(speed * 0xFFFF)
        pca.channels[channel2].duty_cycle = 0
    elif speed < 0:
        # Reverse
        pca.channels[channel1].duty_cycle = 0
        pca.channels[channel2].duty_cycle = int(-speed * 0xFFFF)
    else:
        # Stop
        pca.channels[channel1].duty_cycle = 0
        pca.channels[channel2].duty_cycle = 0

def enable_motor():
    pca.channels[ENA_CHANNEL_1].duty_cycle = 0xFFFF  # Full speed
    pca.channels[ENB_CHANNEL_1].duty_cycle = 0xFFFF  # Full speed
    pca.channels[ENA_CHANNEL_2].duty_cycle = 0xFFFF  # Full speed
    pca.channels[ENB_CHANNEL_2].duty_cycle = 0xFFFF  # Full speed

def stop_motor():
    pca.channels[ENA_CHANNEL_1].duty_cycle = 0x00  # zero speed
    pca.channels[ENB_CHANNEL_1].duty_cycle = 0x00  # zero speed
    pca.channels[ENA_CHANNEL_2].duty_cycle = 0x00  # zero speed
    pca.channels[ENB_CHANNEL_2].duty_cycle = 0x00  # zero speed

    set_motor(MOTOR1_IN1, MOTOR1_IN2, 0)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, 0)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, 0)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, 0)

def set_default_posi():
    print("Motors stopped.")
    stop_motor()

    print("Set to neutral position")
    set_servo_angle(SERVO1_CHANNEL, 90)
    set_servo_angle(SERVO2_CHANNEL, 90)
    set_servo_angle(SERVO3_CHANNEL, 90)
    set_servo_angle(SERVO4_CHANNEL, 90)

#         #Servo1 Min-Max (120 - 180)
#         #Servo2 Min-Max (0 - 100 - 180)
#         #Servo3 Min-Max (45 - 180)
#         #Servo4 Min-Max (0 - 90 "clip")

def open_down():
    set_servo_angle(SERVO1_CHANNEL, 115)
    set_servo_angle(SERVO2_CHANNEL, 100)      
    set_servo_angle(SERVO3_CHANNEL, 130)
    set_servo_angle(SERVO4_CHANNEL, 45)

def open_up():
    set_servo_angle(SERVO1_CHANNEL, 135) 
    set_servo_angle(SERVO2_CHANNEL, 100)
    set_servo_angle(SERVO3_CHANNEL, 70)
    set_servo_angle(SERVO4_CHANNEL, 45)  

def close_down():
    set_servo_angle(SERVO1_CHANNEL, 115) 
    set_servo_angle(SERVO2_CHANNEL, 100)
    set_servo_angle(SERVO3_CHANNEL, 130)
    set_servo_angle(SERVO4_CHANNEL, 95)

def close_up():
    set_servo_angle(SERVO1_CHANNEL, 135) 
    set_servo_angle(SERVO2_CHANNEL, 100)
    set_servo_angle(SERVO3_CHANNEL, 70)
    set_servo_angle(SERVO4_CHANNEL, 95)

def move_forward():
    enable_motor()
    set_motor(MOTOR1_IN1, MOTOR1_IN2, 0.25)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, 0.25)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, 0.25)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, 0.25)
    time.sleep(0.05)
    stop_motor()

def move_backward():
    enable_motor()
    set_motor(MOTOR1_IN1, MOTOR1_IN2, -0.25)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, -0.25)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, -0.25)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, -0.25)
    time.sleep(0.05)
    stop_motor()

def turn_left():
    enable_motor()
    set_motor(MOTOR1_IN1, MOTOR1_IN2, 0.25)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, -0.25)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, -0.25)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, 0.25)
    time.sleep(0.05)
    stop_motor()

def turn_right():
    enable_motor()
    set_motor(MOTOR1_IN1, MOTOR1_IN2, -0.25)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, 0.25)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, 0.25)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, -0.25)
    time.sleep(0.05)
    stop_motor()

def slide_left():
    enable_motor()
    set_motor(MOTOR1_IN1, MOTOR1_IN2, 0.25)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, -0.25)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, 0.25)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, -0.25)
    time.sleep(0.05)
    stop_motor()

def slide_right():
    enable_motor()
    set_motor(MOTOR1_IN1, MOTOR1_IN2, -0.25)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, 0.25)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, -0.25)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, 0.25)
    time.sleep(0.05)
    stop_motor()

def squeeze():
    open_up()
    time.sleep(0.2)
    open_down()
    time.sleep(0.2)
    close_down()
    time.sleep(0.2)
    close_up()

def release():
    open_up()
    time.sleep(0.25)
    close_up()

  

set_default_posi()

# GUI setup
root = tk.Tk()
root.title("Robot Controller")

# Motor control buttons
btn_forward = tk.Button(root, text="Forward", command=move_forward)
btn_backward = tk.Button(root, text="Backward", command=move_backward)
btn_left = tk.Button(root, text="Turn Left", command=turn_left)
btn_right = tk.Button(root, text="Turn Right", command=turn_right)
btn_slide_left = tk.Button(root, text="Slide Left", command=slide_left)
btn_slide_right = tk.Button(root, text="Slide Right", command=slide_right)
btn_stop = tk.Button(root, text="Stop", command=set_default_posi)
btn_open_up = tk.Button(root, text="Open_up", command=open_up)

btn_forward.grid(row=0, column=2)
btn_backward.grid(row=2, column=2)
btn_left.grid(row=1, column=1)
btn_right.grid(row=1, column=3)
btn_slide_left.grid(row=1, column=0)
btn_slide_right.grid(row=1, column=4)
btn_stop.grid(row=1, column=2)

btn_open_up.grid(row=3, column=4)

# Servo control buttons
btn_squeeze = tk.Button(root, text="Squeeze", command=squeeze)
btn_release = tk.Button(root, text="Release", command=release)

btn_squeeze.grid(row=3, column=1)
btn_release.grid(row=3, column=3)

root.mainloop()

# movements_90 = [
#     (SERVO1_CHANNEL, 90, 45),
#     (SERVO3_CHANNEL, 90, 45)
# ]

# movements_180 = [
#     (SERVO1_CHANNEL, 180, 45),
#     (SERVO3_CHANNEL, 180, 45)
# ]

# while True:
#     move_servos_simultaneously(movements_90)
#     time.sleep(1)
#     move_servos_simultaneously(movements_180)
#     time.sleep(1)



# current_angles = {}

# def set_servo_angle(channel, target_angle, velocity):
#     # min_pulse = 0.7  # Adjust if needed
#     # max_pulse = 2.75  # Adjust if needed

#     # pulse_length = min_pulse + (angle / 180.0) * (max_pulse - min_pulse)
#     # duty_cycle = int((pulse_length / 20.0) * 0xFFFF)
#     # pca.channels[channel].duty_cycle = duty_cycle

#     """
#     Move the servo to the specified target angle at the specified velocity.
    
#     :param channel: The PCA9685 channel the servo is connected to.
#     :param target_angle: The target angle to move the servo to (0 to 180 degrees).
#     :param velocity: The angular velocity in degrees per second.
#     """
#     # Read the current position (This would be where you keep track of servo position if needed)
#     current_angle = current_angles.get(channel, 0)
    
#     # Calculate pulse length limits
#     min_pulse = 0.7  # Minimum pulse length in milliseconds (1ms for 0 degrees)
#     max_pulse = 2.75  # Maximum pulse length in milliseconds (2ms for 180 degrees)

#     # Determine the direction to move
#     step = 1 if target_angle > current_angle else -1
    
#     # Move the servo in small increments
#     while current_angle != target_angle:
#         current_angle += step
#         pulse_length = min_pulse + (current_angle / 180.0) * (max_pulse - min_pulse)
#         duty_cycle = int((pulse_length / 20.0) * 0xFFFF)
#         pca.channels[channel].duty_cycle = duty_cycle
        
#         # Update the current angle in the dictionary
#         current_angles[channel] = current_angle
        
#         # Time to wait between steps
#         time.sleep(1.0 / velocity)  # velocity is in degrees per second
        
#         if (step == 1 and current_angle >= target_angle) or (step == -1 and current_angle <= target_angle):
#             break


# def move_servos_simultaneously(movements):
#     """
#     Move multiple servos simultaneously.
    
#     :param movements: A list of tuples, each containing (channel, target_angle, velocity)
#     """
#     threads = []
#     for movement in movements:
#         channel, target_angle, velocity = movement
#         t = threading.Thread(target=set_servo_angle, args=(channel, target_angle, velocity))
#         t.start()
#         threads.append(t)

#     # Wait for all threads to complete
#     for t in threads:
#         t.join()

# try:
#     while True:
#         print("Loop: ", loop)
        

        
#         open_up()
#         time.sleep(0.1)
#         open_down()
#         time.sleep(0.1)
#         close_down()
#         time.sleep(0.1)
#         close_up()
#         time.sleep(3)

#         open_up()
#         time.sleep(0.25)
#         close_up()
#         time.sleep(0.5)
        

#         loop = loop + 1

# except KeyboardInterrupt:
#     print("Turn off all motors on exit")
#     set_motor(MOTOR1_IN1, MOTOR1_IN2, 0)
#     set_motor(MOTOR2_IN1, MOTOR2_IN2, 0)
#     set_motor(MOTOR3_IN1, MOTOR3_IN2, 0)
#     set_motor(MOTOR4_IN1, MOTOR4_IN2, 0)

#     print("Set to neutral position")
#     set_servo_angle(SERVO1_CHANNEL, 90)
#     set_servo_angle(SERVO2_CHANNEL, 90)
#     set_servo_angle(SERVO3_CHANNEL, 90)
#     set_servo_angle(SERVO4_CHANNEL, 90)
#     print("Motors stopped.")