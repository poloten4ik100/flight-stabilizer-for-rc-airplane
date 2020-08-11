from multiprocessing import Process, Queue
import json
import math

from adafruit_servokit import ServoKit

from mpu6050 import MPU6050
from pid import PID
from serialReader import reader
from control import Control
from a_b_filter import ABFilter

# Channel numbers
CHAN_ROLL = 1
CHAN_PITCH = 2
CHAN_VARIATOR = 3
CHAN_STABILIZER_SWITCH = 4

# the ports of the servos on PCA9685
PORT_SERVO_ROLL = 0
PORT_SERVO_PITCH = 1

# On/Off airplane stabilizer
stabilizer: bool = False

# Control result in degress
pid_roll: int = PID(2.53, 0.0001, 1.02)
pid_pitch: int = PID(2.53, 0.0001, 1.02)

# Setpoint in degrees
target_roll: int = 0
target_pitch: int = 0
abfilter_k: float = 0

# Process variable in degrees
controll_roll: int = 0
controll_pitch: int = 0

kit = ServoKit(channels=16)

controls = {}

mpu = MPU6050()

filterRoll = ABFilter(0.01)
filterPitch = ABFilter(0.01)

q = Queue()
uart_proc = Process(name='uart reader', target=reader, args=(q,))
uart_proc.start()

try:
    with open('controller.json') as f:
        channels = json.load(f)
        for ch_id, params in channels.items():
            controls.update({int(ch_id): Control(params[0], params[1])})
except FileNotFoundError:
    print("File not found")

print("                 Roll                Pitch       ")
print("stab, k | angle, target, PID | angle, target, PID")

while True:

    while not q.empty():

        chan, value = q.get()

        if chan == CHAN_ROLL:
            target_roll = controls[chan].degree(value) - 90
        elif chan == CHAN_PITCH:
            target_pitch = controls[chan].degree(value) - 90
        elif chan == CHAN_STABILIZER_SWITCH:
            stabilizer = controls[chan].switch(value)
        elif chan == CHAN_VARIATOR:
            abfilter_k = controls[chan].variator(value, 0.01, 0.9)
            filterRoll.k = abfilter_k
            filterPitch.k = abfilter_k

    gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = mpu.get_data()

    roll = (math.atan2(accel_y, math.sqrt(accel_z ** 2 + accel_x ** 2)) * 180) / math.pi
    pitch = (math.atan2((-1) * accel_x, math.sqrt(accel_z ** 2 + accel_y ** 2)) * 180) / math.pi

    value_roll = filterRoll.filter(gyro_x, roll)
    value_pitch = filterPitch.filter(gyro_y, pitch)

    if stabilizer:
        controll_roll = int(pid_roll.compute(target_roll, value_roll)) + 90
        controll_pitch = int(pid_pitch.compute(target_pitch, value_pitch)) + 90
    else:
        controll_roll = target_roll + 90
        controll_pitch = target_pitch + 90

    stab_status = "OFF"
    if stabilizer:
        stab_status = "ON"

    print(stab_status, abfilter_k, end=" | ")
    print(value_roll, "   ", target_roll, "   ", controll_roll, end=" | ")
    print(value_pitch, "    ", target_pitch, "    ", controll_pitch, end="     \r")

    kit.servo[PORT_SERVO_ROLL].angle = controll_roll
    kit.servo[PORT_SERVO_PITCH].angle = controll_pitch
