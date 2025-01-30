from picarx import Picarx
import time
import scipy.stats as stats # type: ignore
import numpy as np
import math

class LineLocalizer:
    def __init__(self, dark_thresh, light_thresh, steering_scale):
        self.light_thresh = light_thresh
        self.dark_thresh = dark_thresh
        self.thresh_center = (light_thresh - dark_thresh) / 1.25
        self.scale = steering_scale
        self.dark_size = self.thresh_center - self.dark_thresh
        self.light_size = self.light_thresh - self.thresh_center
        
    def get_position(self, sample):
        c = sample[1]
        if c > self.thresh_center:
            ratio = (self.dark_size - (c - self.dark_thresh)) / self.dark_size
            ratio = min(math.pow(ratio, 4), 1)
        else:
            ratio = (self.light_size - (self.light_thresh - c)) / self.light_size
            ratio = -min(math.pow(ratio, 4), 1)
        return ratio * self.scale
        
        
        
px = Picarx()
lx = LineLocalizer(190, 750, 60)
px.forward(5)
while True:
    angle = lx.get_position(px.get_grayscale_data())
    px.set_dir_servo_angle(angle)