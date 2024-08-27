#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

PLD_PIN = 6
BUZZER_PIN = 20
SHUTDOWN_PIN = 26

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PLD_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SHUTDOWN_PIN, GPIO.OUT)

def beep_buzzer(duration=5):
    end_time = time.time() + duration
    while time.time() < end_time:
        GPIO.output(BUZZER_PIN, 1)
        time.sleep(1)
        GPIO.output(BUZZER_PIN, 0)
        time.sleep(1)

def shutdown_pi():
    print("bye 4 now...")
    GPIO.output(SHUTDOWN_PIN, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(SHUTDOWN_PIN, GPIO.LOW)

def my_callback(channel):
    if GPIO.input(PLD_PIN):  # PLD_PIN == 1
        print("UPS engaged!")
        print("5 seconds...")
        beep_buzzer(5)
        shutdown_pi()
    else:  # PLD_PIN != 1
        print("Power OK")

GPIO.add_event_detect(PLD_PIN, GPIO.BOTH, callback=my_callback)
print("UPC Started")

GPIO.cleanup()
