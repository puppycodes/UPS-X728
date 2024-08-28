#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("ups init.")

PLD_PIN = 6         # Power Loss
CHARGE_PIN = 16     # Charging
BUZZER_PIN = 20     # Buzzer
SHUTDOWN_PIN = 26   # Shutdown

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PLD_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SHUTDOWN_PIN, GPIO.OUT)
GPIO.setup(CHARGE_PIN, GPIO.OUT)

# force charge to low at first
GPIO.output(CHARGE_PIN, GPIO.LOW)
logging.info("start charge pin low...")

# global, dont forget to float
SHUTDOWN_COUNTDOWN = 30.0

# buzz style
BUZZ_DURATION = 0.3  # seconds per buzz
BUZZ_INTERVAL = 0.3  # seconds between buzzes
BUZZ_COUNT = 2  # Number of buzzes

def beep_buzzer(buzz_count=1, buzz_duration=BUZZ_DURATION, buzz_interval=BUZZ_INTERVAL):
    logging.info(f"buzzzzing {buzz_count} times.")
    for _ in range(buzz_count):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(buzz_duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(buzz_interval)

def shutdown_pi():
    logging.info("shutting down...")
    time.sleep(1) # stern look
    GPIO.output(SHUTDOWN_PIN, GPIO.HIGH)
    time.sleep(3)  # sterner look
    GPIO.output(SHUTDOWN_PIN, GPIO.LOW)
    logging.info("continue with shutdown...")

def shutdown_sequence():
    start_time = time.time()
    end_time = start_time + SHUTDOWN_COUNTDOWN
    next_buzz_time = start_time
    buzzes_remaining = BUZZ_COUNT

    logging.info(f"off in {SHUTDOWN_COUNTDOWN}...")
    while time.time() < end_time:
        current_time = time.time()

        # buzzz it
        if current_time >= next_buzz_time and buzzes_remaining > 0:
            beep_buzzer()  # bee
            next_buzz_time = current_time + BUZZ_INTERVAL  # next bee
            buzzes_remaining -= 1

        time.sleep(0.5)  # be kind

    shutdown_pi()

def pld(channel):
    if GPIO.input(PLD_PIN):
        logging.info("UPS engaged! Initiating shutdown sequence...")
        time.sleep(1)
        shutdown_sequence()
    else:
        logging.info("UPS OK")

GPIO.add_event_detect(PLD_PIN, GPIO.BOTH, callback=pld, bouncetime=500)  # watchful debounce
logging.info("watching UPS")

try:
    while True: # keep going for systemd
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("interrupting cow")
except Exception as e:
    logging.error(f"uh oh: {e}")
finally:
    GPIO.cleanup()
    logging.info("cleanup GPIO")