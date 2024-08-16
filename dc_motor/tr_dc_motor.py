import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Create the I2C bus interface
i2c = busio.I2C(SCL, SDA)

# Create a PCA9685 object
pca = PCA9685(i2c)
pca.frequency = 60  # Set frequency to 60 Hz for motor control

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

pca.channels[ENA_CHANNEL_1].duty_cycle = 0xFFFF  # Full speed
pca.channels[ENB_CHANNEL_1].duty_cycle = 0xFFFF  # Full speed
pca.channels[ENA_CHANNEL_2].duty_cycle = 0xFFFF  # Full speed
pca.channels[ENB_CHANNEL_2].duty_cycle = 0xFFFF  # Full speed

loop = 0

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

def stop_motor():
    pca.channels[ENA_CHANNEL_1].duty_cycle = 0x00  # zero speed
    pca.channels[ENB_CHANNEL_1].duty_cycle = 0x00  # zero speed
    pca.channels[ENA_CHANNEL_2].duty_cycle = 0x00  # zero speed
    pca.channels[ENB_CHANNEL_2].duty_cycle = 0x00  # zero speed

    set_motor(MOTOR1_IN1, MOTOR1_IN2, 0)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, 0)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, 0)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, 0)

try:
    print("Run all motors forward")
    set_motor(MOTOR1_IN1, MOTOR1_IN2, -0.25)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, 0.25)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, 0.25)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, -0.25)

    time.sleep(0.25)

    stop_motor()

except KeyboardInterrupt:
    # Turn off all motors on exit
    set_motor(MOTOR1_IN1, MOTOR1_IN2, 0)
    set_motor(MOTOR2_IN1, MOTOR2_IN2, 0)
    set_motor(MOTOR3_IN1, MOTOR3_IN2, 0)
    set_motor(MOTOR4_IN1, MOTOR4_IN2, 0)
    print("Motors stopped.")
