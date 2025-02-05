import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
from picarx import Picarx
from scipy import ndimage

px = Picarx()

cap_shape = (480, 640, 3)
cap = cv2.VideoCapture('/dev/video0')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_shape[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_shape[0])

px.set_cam_tilt_angle(-40)
px.forward(30)

# Loop over all frames captured by camera indefinitely
while True:
	ret, frame = cap.read()
	frame = frame.reshape(cap_shape)
	frame = frame[150:]
	
	thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	_, thresh = cv2.threshold(thresh, 60, 255, cv2.THRESH_BINARY_INV)
	mass = ndimage.center_of_mass(thresh)[1] - (thresh.shape[1] / 2)
	if mass < 0: mass = max(thresh.shape[1] / -2, mass)
	if mass > 0: mass = min(thresh.shape[1] / 2, mass)
	ratio = (mass / thresh.shape[1]) * 120
	# print(ratio)

	px.set_dir_servo_angle(ratio)