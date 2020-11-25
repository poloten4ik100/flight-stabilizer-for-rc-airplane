from multiprocessing import Process, Queue
import json
import math
import sys
import logging
import time

from adafruit_servokit import ServoKit

from mpu6050 import MPU6050
from pid import PID
from serialReader import reader
from control import Control
from a_b_filter import ABFilter
from indicator import Indicator


FILE_NAME_LOG = "airplane.log"

FILE_NAME_CALIBRATION = "controller.json"

# Channel numbers
CHAN_ROLL = 1
CHAN_PITCH = 2
CHAN_VARIATOR = 3
CHAN_STABILIZER_SWITCH = 4

# the ports of the servos on PCA9685
PORT_SERVO_ROLL = 0
PORT_SERVO_PITCH = 1

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
    filename=FILE_NAME_LOG,
    level=logging.DEBUG)
logging.info('airplane controller launch')

# On/Off airplane stabilizer
stabilizer: bool = False
# On/Off airplane stabilizer
stabilizer_mpu: bool = False

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

#Led Init
red = Indicator(24)
green = Indicator(23, True)

try:
    kit = ServoKit(channels=16)
except Exception as identifier:
    logging.error("servo kit error: %s", identifier)
    red.on()
    sys.exit(1)

controls = {}

try:
    mpu = MPU6050()
except Exception as identifier:
    logging.error("gyro/accell error: %s", identifier)
    red.on()
    green.on()
    sys.exit(1)

filterRoll = ABFilter(0.01)
filterPitch = ABFilter(0.01)

q = Queue()
uart_proc = Process(name='uart reader', target=reader, args=(q,))
uart_proc.start()

try:
    with open(FILE_NAME_CALIBRATION) as f:
        channels = json.load(f)
        for ch_id, params in channels.items():
            controls.update({int(ch_id): Control(params[0], params[1])})
except Exception as identifier:
    logging.error("calibration file open error: %s", identifier)

#print("                   Roll                     Pitch          ")
#print("stab, k   | tau, angle, target, PID | tau, angle, target, PID")

logging.info('airplane controller started')

logging.info("data updates every 1 second. format of data:")
logging.info("                             Roll                       Pitch          ")
logging.info("stab,   k     |      tau, angle, tar, PID |        tau, angle, tar, PID")

time_tmp = int(time.time() * 1000)

tau_roll = 0
tau_pitch = 0
value_roll = 0
value_pitch = 0

while True:

    if stabilizer:
        if green.state != "dblink":
            green.blink_double()
    else:
        if green.state != "blink":
            green.blink()

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
    if stabilizer:
        try:
            if not stabilizer_mpu:
                mpu.init_device()
            gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = mpu.get_data()
            stabilizer_mpu = True
        except Exception as identifier:
            if stabilizer_mpu:
                logging.error("gyro/accell reading error: %s", identifier)
            stabilizer_mpu = False
            red.on()
            green.on()
            
    else:
        stabilizer_mpu = False

    stabilizer = stabilizer_mpu

    if stabilizer:
        roll = (math.atan2(accel_y, math.sqrt(accel_z ** 2 + accel_x ** 2)) * 180) / math.pi
        pitch = (math.atan2((-1) * accel_x, math.sqrt(accel_z ** 2 + accel_y ** 2)) * 180) / math.pi

        value_roll, tau_roll = filterRoll.filter(gyro_x, roll)
        value_pitch, tau_pitch = filterPitch.filter(gyro_y, pitch)

        controll_roll = int(pid_roll.compute(target_roll, value_roll)) + 90
        controll_pitch = int(pid_pitch.compute(target_pitch, value_pitch)) + 90
    else:
        controll_roll = target_roll + 90
        controll_pitch = target_pitch + 90

    stab_status = "OFF"
    if stabilizer:
        stab_status = "ON"

    if int(time.time() * 1000) > time_tmp:
        logging.info("%s, k: %s | roll: %s, %s, %d, %d | pitch:  %s, %s, %d, %d",
            stab_status, 
            "{:.3f}".format(abfilter_k),
            "{:.3f}".format(tau_roll),
            "{:.2f}".format(value_roll),
            target_roll,
            controll_roll,
            "{:.3f}".format(tau_pitch),
            "{:.2f}".format(value_pitch),
            target_pitch,
            controll_pitch)
        time_tmp = int(time.time() * 1000) + 500
    #print(stab_status, "{:.3f}".format(abfilter_k), end=" | ")
    #print("{:.3f}".format(tau_roll) + "s", "{:.2f}".format(value_roll), "  ", target_roll, "  ", controll_roll, end=" | ")
    #print("{:.3f}".format(tau_pitch) + "s", "{:.2f}".format(value_pitch), "  ", target_pitch, "  ", controll_pitch, end="     \r")

    try:
        kit.servo[PORT_SERVO_ROLL].angle = controll_roll
        kit.servo[PORT_SERVO_PITCH].angle = controll_pitch
    except Exception as identifier:
        logging.error("servo kit set error: %s", identifier)
        red.on()
        time.sleep(0.5)