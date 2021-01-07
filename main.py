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

try:
    from modules.motor import MotorI2C, DualMI2C
except Exception:
    print("MAIN: Exception Initializing MotorI2C:", sys.exc_info()[0])

# Constatns
red = 0xFF0000
green = 0x00FF00
blue = 0x0000FF
# ---------

print("MAIN: Reading Config")
config = ujson.load(open("default_config.json", "r"))
threads = {}

print("MAIN: Initializing IRQ Functions")
def m_switch():
    if motor_stop.value() == 1:
        _thread.notify(threads["th_cam_to_motor"], _thread.SUSPEND)
    else:
        _thread.notify(threads["th_cam_to_motor"], _thread.RESUME)


print("MAIN: Initializing Motor")
try:
    ml = MotorI2C(i2c_master, 0x08, MotorI2C.offset_motor_1)
    mr = MotorI2C(i2c_master, 0x08, MotorI2C.offset_motor_2)
    m = DualMI2C(ml, mr)
except Exception as e:
    print("MAIN: Exception Initializing MotorI2C:", sys.exc_info()[0])
else:
    ## THREADING
    import _thread
    from threads import thread_cam_to_motor

    print("MAIN: Starting Threads...")
    threads["th_cam_to_motor"] = _thread.start_new_thread("th_cam_to_motor", thread_cam_to_motor.th_cam_to_motor, (threads, i2c_slave, m, config))

    motor_stop = IrqPin(pins["Sens1"], m_switch, trigger=IRQ_ANYEDGE)
