from picarx import Picarx
import json
import math



class LineLocalizer:
    def __init__(self, calibration):
        self.cal = calibration
        
    def bigger(self, a, b, cutoff):
        return abs(a - b) >= cutoff
    
    def littler(self, a, b, cutoff):
        return abs(a - b) <= cutoff

    def sample_normalization(self, sample):
        calibrated = [0, 0, 0]
        for i in range(3):
            top_range = self.cal['max'][i] - self.cal['min'][i]
            adjusted_val = sample[i] - self.cal['min'][i]
            calibrated[i] = int((adjusted_val / top_range) * 1000)
            if calibrated[i] < 0: calibrated[i] = 0
            if calibrated[i] > 1000: calibrated[i] = 1000
        return calibrated
        
    def get_position(self, sample):
        sample = self.sample_normalization(sample)

        ratio = ((sample[0] - sample[1]) / 1000) ** 2
        return ratio * 60    
        
        
px = Picarx()
with open('cal.json', 'r') as file: cal = json.load(file)
lx = LineLocalizer(cal)

px.forward(5)
while True:
    angle = lx.get_position(px.get_grayscale_data())
    # print(angle * 60)
    px.set_dir_servo_angle(angle)