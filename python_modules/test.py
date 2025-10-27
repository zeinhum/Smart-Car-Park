import time

from test2 import PortReader
from vehicle_detection import DetectVehicle

if __name__=="__main__":
    port = DetectVehicle()
    while True:

        port.plate_number()
