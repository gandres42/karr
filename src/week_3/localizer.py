from picarx import Picarx
import time
import scipy.stats as stats # type: ignore

class LineLocalizer:
    def __init__(self, light_thresh, dark_thresh):
        self.light_thresh = light_thresh
        self.dark_thresh = dark_thresh
        
    def get_position(self, sample):
        # print(sample)
        res = stats.linregress(sample, range(len(sample)))
        print(res.slope, res.intercept)
        # return slope * 50
        
        
        
px = Picarx()
lx = LineLocalizer(350, 480)
# px.forward(20)
while True:
    angle = lx.get_position(px.get_grayscale_data())
    # px.set_dir_servo_angle(angle)
# LineLocalizer(350, 450)