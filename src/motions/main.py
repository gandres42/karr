from picarx import Picarx
import time

if __name__ == "__main__":
    px = Picarx()
    
    px.forward(50)
    time.sleep(10)
    px.stop()
