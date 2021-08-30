"""
ToDo:
- Try / Except has to go into motor.py at some point
"""

print("MAIN: Importing Modules")

from modules.functions import *
import sys
from machine import *
# from boot import i2c_slave, i2c_master
import ujson
from modules.irqPin import IrqPin
from modules.pins import pins
import utime
from modules.cuart import CUART
from modules.display import display

try:
    from modules.motor import MotorI2C, DualMI2C
except Exception:
    print("MAIN: Exception Initializing MotorI2C:", sys.exc_info()[0])

print("MAIN: Reading Config")
config = ujson.load(open("default_config.json", "r"))

print("MAIN: Initializing display")
try:
    disp = display(i2c_master)
except Exception as e:
    print("MAIN: Exception Initializing display:\n", e)


threads = {}
#                        type              angle  midfactor     top left     top right    down left    down right
thctm_values = {"line": (CUART.ltype_straight, 0, 0), "green": {"tl": False, "tr": False, "dl": False, "dr": False}, "time": 0}

print("MAIN: Initializing Motor")
disp.debug("Init. Motor")
try:
    ml = MotorI2C(i2c_master, 0x08, MotorI2C.offset_motor_1)
    mr = MotorI2C(i2c_master, 0x08, MotorI2C.offset_motor_2)
    m = DualMI2C(ml, mr)
except Exception as e:
    print("MAIN: Exception Initializing MotorI2C:\n", e)
    disp.debug("Exept. Motor")
else:
    ## THREADING
    import _thread
    from threads import thread_cam_to_motor

    print("MAIN: Starting Threads...")
    disp.debug("Start Threads")
    threads["th_cam_to_motor"] = _thread.start_new_thread("th_cam_to_motor", thread_cam_to_motor.th_cam_to_motor, (threads, thctm_values, m, config, disp))

print("MAIN: Setting up Cuart connection")
disp.debug("Init Cuart")
cuart = CUART(thctm_values, config)  # init using default settings

print("MAIN: Setting default Motor Values to 50 and 50 for testing purposes")
m.move(50, 50)
