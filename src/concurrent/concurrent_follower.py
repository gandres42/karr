import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
from picarx import Picarx
from scipy import ndimage
# concurrent.futures is a wrapper around Thread anyways, so may as well use the lower level one
from threading import Thread, Lock

class Bus:
    def __init__(self):
        self.msg = None
        self.lock = Lock()
        
    def write(self, msg):
        with self.lock:
            self.msg = msg
        
    def read(self):
        with self.lock:
            return self.msg

def scanning_loop(bussin: Bus):
	cap_shape = (480, 640, 3)
	cap = cv2.VideoCapture('/dev/video0')
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_shape[1])
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_shape[0])
	while True:
		ret, frame = cap.read()
		frame = frame.reshape(cap_shape)
		frame = frame[150:]
		
		thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		_, thresh = cv2.threshold(thresh, 80, 255, cv2.THRESH_BINARY_INV)
		mass = ndimage.center_of_mass(thresh)[1] - (thresh.shape[1] / 2)
		if mass < 0: mass = max(thresh.shape[1] / -2, mass)
		if mass > 0: mass = min(thresh.shape[1] / 2, mass)
		angle = (mass / thresh.shape[1]) * 100
		bussin.write(angle)

def control_loop(bussin_respectfully: Bus):
    px = Picarx()
    px.set_cam_tilt_angle(-40)
    while bussin_respectfully.read() is None:
        time.sleep(1/60)
    px.forward(30)
    while True:
        angle = bussin_respectfully.read()
        px.set_dir_servo_angle(angle)
        time.sleep(1/60)

bus = Bus()
Thread(target=scanning_loop, daemon=True, args=(bus, )).start()
Thread(target=control_loop, daemon=True, args=(bus, )).start()

try:
	while True:
		pass
except KeyboardInterrupt:
    exit()