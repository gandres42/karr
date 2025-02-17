import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
from picarx import Picarx
from scipy import ndimage
# concurrent.futures is a wrapper around Thread anyways, so may as well use the lower level one
from threading import Thread, Lock, Event
from rossros import Bus # type: ignore

def line_following_loop(death: Event, steering_bus: Bus):
    cap_shape = (480, 640, 3)
    cap = cv2.VideoCapture('/dev/video0')
    fps = cap.set(cv2.CAP_PROP_FPS, 10)
    while not death.is_set():
        ret, frame = cap.read()
        frame = frame.reshape(cap_shape)
        frame = frame[150:]

        thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(thresh, 80, 255, cv2.THRESH_BINARY_INV)
        mass = ndimage.center_of_mass(thresh)[1] - (thresh.shape[1] / 2)
        if mass < 0: mass = max(thresh.shape[1] / -2, mass)
        if mass > 0: mass = min(thresh.shape[1] / 2, mass)
        angle = (mass / thresh.shape[1]) * 100
        steering_bus.set_message(angle)
        # time.sleep(1/20)

def object_detection_loop(death: Event, distance_bus: Bus, px: Picarx):
    while not death.is_set():
        dist = px.get_distance()
        distance_bus.set_message(dist)
        # time.sleep(1/10)

def control_loop(death: Event, distance_bus: Bus, steering_bus: Bus, px: Picarx):
    px.set_cam_tilt_angle(-40)
    while steering_bus.get_message() is None:
        time.sleep(1/60)
    moving = True
    px.forward(10)
    while True:
        if distance_bus.get_message() <= 10: # type: ignore
            if moving:
                px.stop()
                moving = False
        else:
            if not moving:
                px.forward(10)
                moving = True
        px.set_dir_servo_angle(steering_bus.get_message())

distance_bus = Bus()
distance_bus.set_message(0)
steering_bus = Bus()
steering_bus.set_message(None)
death = Event()
px = Picarx()
px_lock = Lock()

Thread(target=line_following_loop, args=(death, steering_bus, )).start()
Thread(target=object_detection_loop, args=(death, distance_bus, px)).start()
Thread(target=control_loop, args=(death, distance_bus, steering_bus, px)).start()

try:
	while True:
		pass
except KeyboardInterrupt:
    death.set()
    exit()