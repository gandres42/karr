from picarx import Picarx
import math
import os
import time
import json
import matplotlib.pyplot as plt
import numpy as np

px = Picarx()
time.sleep(1)
print('go!')
samples = []
try:
    while True:
        samples.append(px.get_grayscale_data())
except KeyboardInterrupt:
    pass




# sorted_data = sorted(samples, key=lambda x: x[0])
samples = np.array(samples)
mins = [np.percentile(samples[:, 0], 1), np.percentile(samples[:, 1], 1), np.percentile(samples[:, 2], 1)]
maxs = [np.percentile(samples[:, 0], 99), np.percentile(samples[:, 1], 99), np.percentile(samples[:, 2], 99)]

cal = {
    "min": mins,
    "max": maxs
}

with open('cal.json', 'w') as f:
    json.dump(cal, f)