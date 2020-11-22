from multiprocessing import Process
import RPi.GPIO as GPIO
from time import sleep


class Indicator():
    def __init__(self, pin, init=False):
        self.pin = pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
        GPIO.setup(self.pin, GPIO.OUT, initial=GPIO.LOW)
        self.blink_proc = Process(name='led blink', target=self._blink)
        self.blink_double_proc = Process(name='led blink double', target=self._blink_double)
        self.state = None
        if init:
            self.on()
            sleep(0.5)
            self.off()
            sleep(0.5)
            self.on()
            sleep(0.5)
            self.off()

    def on(self):
        self.stop()
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = "on"

    def off(self):
        self.stop()
        GPIO.output(self.pin, GPIO.LOW)
        self.state = "off"

    def blink(self):
        self.stop()
        if not self.blink_proc.is_alive():
            self.blink_proc = Process(name='led blink', target=self._blink)
            self.blink_proc.start()
            self.state = "blink"

    def blink_double(self):
        self.stop()
        if not self.blink_double_proc.is_alive():
            self.blink_double_proc = Process(name='led blink double', target=self._blink_double)
            self.blink_double_proc.start()
            self.state = "dblink"

    def stop(self):
        if self.blink_proc.is_alive():
            self.blink_proc.terminate()
            GPIO.output(self.pin, GPIO.LOW)
            self.state = None
        if self.blink_double_proc.is_alive():
            self.blink_double_proc.terminate()
            GPIO.output(self.pin, GPIO.LOW)
            self.state = None

    def _blink(self):
        while True:
            GPIO.output(self.pin, GPIO.HIGH)
            sleep(0.01)
            GPIO.output(self.pin, GPIO.LOW)
            sleep(0.99)

    def _blink_double(self):
        while True:
            GPIO.output(self.pin, GPIO.HIGH)
            sleep(0.01)
            GPIO.output(self.pin, GPIO.LOW)
            sleep(0.18)
            GPIO.output(self.pin, GPIO.HIGH)
            sleep(0.01)
            GPIO.output(self.pin, GPIO.LOW)
            sleep(0.80)

    def __del__(self):
        self.stop()
