from modules.ssd1306 import SSD1306_I2C
import _thread
from threads.thread_messages import thread_messages as thr_msg
from modules.functions import *
import utime
from modules.cuart import CUART
from machine import Timer


class display(SSD1306_I2C):
    line1 = {"batteryVoltage": 3.7, "leftMotor": 30, "rightMotor": 30}
    line2 = {"cuartAngle": 20, "cuartMidfactor": 4, "cuartType": "Straight", "cuartDots": [False, True, False, False]}
    line3 = ""
    line4 = ""
    def __init__(self, i2c, width=128, height=64, addr=0x3c, external_vcc=False):
        self.timer = Timer(0)
        self.timer.init(period=100, callback=self.refresh)
        super().__init__(width, height, i2c, addr, external_vcc)

        # Battery logo Top Left
        self.draw_rect(4, 3, 15, 12)
        self.draw_rect(2, 5, 4, 9)
        self.draw_rect(4, 6, 4, 8, color=0)
        self.show()

    def draw_battery(self):
        # Battery logo Top Left
        self.draw_rect(4, 3, 15, 12)
        self.draw_rect(2, 5, 4, 9)
        self.draw_rect(4, 6, 4, 8, color=0)
        self.show()

    def refresh(self):
        self.fill(0)
        self.draw_battery()

        self.text("{0} {1: >6} {2: }".format(self.line1["batteryVoltage"], self.line1["leftMotor"], self.line1["rightMotor"]), 0, 18)
        
        self.text("{0: 03d} {1: 02d} {2}".format(self.line2["cuartAngle"], self.line2["cuartMidfactor"], CUART.ltype_strings[self.line2["cuartType"]]), 16, 0)

        self.text(self.line3, 32, 0)

        self.text(self.line4, 48, 0)

    def debug(self, text):
        self.line3 = self.line4
        self.line4 = text
        