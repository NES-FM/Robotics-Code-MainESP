from modules.ssd1306 import SSD1306_I2C
import _thread
from threads.thread_messages import thread_messages as thr_msg
from modules.functions import *
import utime
from modules.cuart import CUART
from machine import Timer


class display(SSD1306_I2C):
    line1 = {"batteryVoltage": 3.7, "leftMotor": 30, "rightMotor": 30}
    line2 = {"cuartAngle": 20, "cuartMidfactor": 4, "cuartType": CUART.ltype_straight, "cuartDots": [False, True, False, False]}
    cuart_sensor_array = []
    line3 = ""
    line4 = ""
    clock_pixel_status = False
    def __init__(self, i2c, width=128, height=64, addr=0x3c, external_vcc=False):
        self.timer = Timer(0)
        self.timer.init(period=100, callback=self.refresh)
        super().__init__(width, height, i2c, addr, external_vcc)

        self.draw_battery()
        self.show()

    def draw_battery(self):
        # Battery logo Top Left
        self.draw_rect(4, 3, 15, 12)
        self.draw_rect(2, 5, 4, 9)
        self.draw_rect(4, 6, 4, 8, color=0)

    def draw_sensor_array(self):
        self.draw_rect(17, 29, 66, 32)
        i = 18
        for x in self.cuart_sensor_array:
            self.draw_rect(i, 30, i+1, 31, x)
            i += 2

    def refresh(self, x):
        try:
            self.fill(0)

            self.draw_battery()

            self.text("{0}    {1:+} {2:+}".format(self.line1["batteryVoltage"], self.line1["leftMotor"], self.line1["rightMotor"]), 18, 0)

            self.text("{0:+03d} {1:+02d} {2}".format(self.line2["cuartAngle"], self.line2["cuartMidfactor"], CUART.ltype_strings.get(self.line2["cuartType"], "UNKNOWN")), 0, 16)

            self.draw_sensor_array()

            self.text(self.line3, 0, 35)

            self.text(self.line4, 0, 51)
            
            self.pixel(127,63,self.clock_pixel_status)
            self.clock_pixel_status = not self.clock_pixel_status

            self.show()
        except:
            pass

    def set_values_thctm(self, lmotor, rmotor, cangle, cmidfactor, ctype, cuart_sensor_array = None, cdots = None):
        self.line1["leftMotor"] = lmotor
        self.line1["rightMotor"] = rmotor
        self.line2 = {"cuartAngle": cangle, "cuartMidfactor": cmidfactor, "cuartType": ctype}
        if cuart_sensor_array is not None: self.cuart_sensor_array = cuart_sensor_array.copy()
        if cdots is not None: self.line2["cuartDots"] = cdots.copy()

    def set_bvoltage(self, bvoltage):
        self.line1["batteryVoltage"] = bvoltage

    def debug(self, text):
        self.line3 = self.line4
        self.line4 = text
        