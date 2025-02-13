
# import time
# import cv2
# import numpy as np
from scipy import ndimage
# # concurrent.futures is a wrapper around Thread anyways, so may as well use the lower level one
# from threading import Thread, Lock

# cap_shape = (480, 640, 3)
# cap = cv2.VideoCapture('http://karr:8080/stream')

# while True:
#     ret, frame = cap.read()
#     # frame = frame.reshape(cap_shape)
#     frame = frame[150:]
    


import cv2

# URL of the online stream (replace with your actual stream URL)
stream_url = "http://karr:8080/stream"

# Open the video stream
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to retrieve frame")
        break

    # Show the frame
    
    thresh = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(thresh, 80, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("frick", thresh)
    mass = ndimage.center_of_mass(thresh)[1] - (thresh.shape[1] / 2)
    cv2.imshow("Online Stream", thresh)
    if mass < 0: mass = max(thresh.shape[1] / -2, mass)
    if mass > 0: mass = min(thresh.shape[1] / 2, mass)
    angle = (mass / thresh.shape[1]) * 100

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
