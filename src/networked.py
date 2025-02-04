import time
from networktables import NetworkTables
import subprocess
import signal
import time
import os
from picarx import Picarx

NetworkTables.initialize()
sd = NetworkTables.getTable("karr")
px = Picarx()

# start camera stream
ustreamer = subprocess.Popen(["ustreamer", "/dev/video0", "-s", "0.0.0.0"], preexec_fn=os.setsid)

try:
    current_vel = 0
    while True:
        vel = sd.getNumber("drive", 0)
        if current_vel != vel:
            current_vel = vel
            if vel > 0: px.forward(int(vel))
            elif vel < 0: px.backward(int(vel))
            else: px.stop()
        
finally:
    os.killpg(os.getpgid(ustreamer.pid), signal.SIGTERM)
