from modules.rotary_irq_esp import RotaryIRQ
from machine import I2C, Pin, Timer
from modules import ssd1306


class Display():
    def __init__(self, rot_clk=26, rot_dt=27, btn=25, disp_i2c=I2C(-1, sda=Pin(21), scl=Pin(22))):
        self.rot = RotaryIRQ(pin_num_clk=rot_clk,
                             pin_num_dt=rot_dt,
                             min_val=0,
                             max_val=3,
                             reverse=True,
                             range_mode=RotaryIRQ.RANGE_WRAP)
        self.rot_old_val = -1

        self.timer = Timer(0)
        self.btn = Pin(btn, Pin.IN)
        self.btn_irq = self.btn.irq(self.btn_irq, Pin.IRQ_RISING)
        self.btn_value = False
        self.selected = 0

        self.disp = ssd1306.SSD1306_I2C(128, 64, disp_i2c)
        self.disp.fill(0)
        self.disp.show()

        self.offset = 4
        self.line1 = 12
        self.line = 9
        self.space = 3

        self.disp_config = [
            [{"x": 0, "y": self.offset + self.line1}, {"x": 64, "y": self.offset + self.line1}],
            [{"x": 0, "y": self.offset + self.line1 + self.line + self.space}, {"x": 64, "y": self.offset + self.line1 + self.line + self.space}],
            [{"x": 0, "y": self.offset + self.line1 + self.line * 2 + self.space * 2}, {"x": 64, "y": self.offset + self.line1 + self.line * 2 + self.space * 2}],
            [{"x": 0, "y": self.offset + self.line1 + self.line * 3 + self.space * 3}, {"x": 64, "y": self.offset + self.line1 + self.line * 3 + self.space * 3}]
        ]
        self.disp_text = [
            ("R", ""),
            ("G", ""),
            ("B", ""),
            ("Mot", "")
        ]
        self.disp_options = [
            {"val_min": 0, "val_max": 255, "curr": 0},
            {"val_min": 0, "val_max": 255, "curr": 255},
            {"val_min": 0, "val_max": 255, "curr": 0},
            {"val_min": -100, "val_max": 100, "curr": 0}
        ]
        self.disp_right = False
        self.disp_title = "Some Title"
        self.refresh()

    def refresh(self):
        rot_val = self.rot.value()
        if self.btn_value is True:
            self.btn_value = False
            self.disp_right = not self.disp_right

            if self.disp_right is True:
                self.selected = rot_val
                self.redraw()
                conf = self.disp_config[rot_val][1]
                self.disp.draw_rect(conf["x"], conf["y"], conf["x"] + 62, conf["y"] + self.line)
                self.disp.text(str(self.disp_options[rot_val]["curr"]), 64, self.offset + self.line1 + self.line * rot_val + self.space * rot_val, 0)
                self.disp.show()
                self.rot.set(value=self.disp_options[rot_val]["curr"], min_val=self.disp_options[rot_val]["val_min"], max_val=self.disp_options[rot_val]["val_max"])

            else:
                self.redraw()
                conf = self.disp_config[self.selected][0]
                self.disp.draw_rect(conf["x"], conf["y"], conf["x"] + 62, conf["y"] + self.line)
                self.disp.text(self.disp_text[self.selected][0], 0, self.offset + self.line1 + self.line * self.selected + self.space * self.selected, 0)
                self.disp.show()
                self.rot.set(value=self.selected, min_val=0, max_val=4)

        if self.rot_old_val != rot_val:
            if self.disp_right:
                self.disp_options[self.selected]["curr"] = rot_val
                self.redraw()
                conf = self.disp_config[self.selected][1]
                self.disp.draw_rect(conf["x"], conf["y"], conf["x"] + 62, conf["y"] + self.line)
                self.disp.text(str(self.disp_options[self.selected]["curr"]), 64, self.offset + self.line1 + self.line * self.selected + self.space * self.selected, 0)
                self.disp.show()
                self.rot_old_val = rot_val
            else:
                self.redraw()
                conf = self.disp_config[rot_val][0]
                self.disp.draw_rect(conf["x"], conf["y"], conf["x"] + 62, conf["y"] + self.line)
                self.disp.text(self.disp_text[rot_val][0], 0, self.offset + self.line1 + self.line * rot_val + self.space * rot_val, 0)
                self.disp.show()
                self.rot_old_val = rot_val

    def redraw(self):
        self.disp.fill(0)
        self.disp.text(self.disp_title, 0, self.offset)
        i = 0
        for row in self.disp_text:
            right_col = False
            for col in row:
                if right_col:
                    self.disp.text(str(self.disp_options[i]["curr"]), 64, self.offset + self.line1 + self.line * i + self.space * i)
                else:
                    self.disp.text(col, 0, self.offset + self.line1 + self.line * i + self.space * i)
                right_col = True
            i += 1
        self.disp.draw_line(63, self.offset + self.line1, 64, 64)
        self.disp.draw_line(1, 14, 128, 14)
        self.disp.show()

    def btn_irq(self, pin):
        self.timer.init(mode=Timer.ONE_SHOT, period=1, callback=self.btn_timer_irq)

    def btn_timer_irq(self, timer):
        self.btn_value = True
