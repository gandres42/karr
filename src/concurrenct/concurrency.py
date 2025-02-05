from picarx import Picarx
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
    