# from machine import PWM, Pin, Timer, I2C
from micropython import const
from modules.functions import *
# import time


# class Motor:
#
#     FORWARD = const(0)
#     BACKWARD = const(1)
#
#     def __init__(self, pwm_pin=4, p1_pin=17, p2_pin=16, reverse=False, rotary_pin=15):
#         self.motor_pwm = PWM(Pin(pwm_pin), duty=0)
#         if reverse is False:
#             self.motor_1 = Pin(p1_pin, Pin.OUT, Pin.PULL_DOWN)
#             self.motor_2 = Pin(p2_pin, Pin.OUT, Pin.PULL_DOWN)
#         else:
#             self.motor_2 = Pin(p1_pin, Pin.OUT, Pin.PULL_DOWN)
#             self.motor_1 = Pin(p2_pin, Pin.OUT, Pin.PULL_DOWN)
#
#         self.motor_pwm.init(freq=5000, duty=0)
#
#         self.moving = False
#         self.pulse = 0
#
#         self.config = reload_config()
#
#         self.PID = {
#             "speed_actual": 0.0,
#             "speed_request": 0,
#             "LOOPTIME": 100,
#             "countOld": 0,
#             "count": 0,
#             "pid_result": 0,
#             "error": 0,
#             "last_error": 0,
#             "PWM_val": 0
#         }
#
#         self.debounce_timer = Timer(0)
#         self.pid_timer = Timer(1)
#         self.pid_timer.init(period=self.PID["LOOPTIME"], mode=Timer.PERIODIC, callback=self.get_motor_data)  # callback=self.motor_pid_correct)
#         self.rotary_interrupt = Pin(rotary_pin)
#         self.rotary_interrupt.irq(trigger=self.rotary_interrupt.IRQ_FALLING, handler=self.rotary_callback)
#
#     def move(self, speed, direction=-1):
#         self.moving = True
#
#         if speed > 100:
#             speed = 100
#         elif speed < -100:
#             speed = -100
#
#         if direction == -1:
#             if speed < 0:
#                 direction = self.BACKWARD
#                 speed = abs(speed)
#             elif speed == 0:
#                 self.stop()
#             elif speed > 0:
#                 direction = self.FORWARD
#         else:
#             if speed == 0:
#                 self.stop()
#             elif speed < 0:
#                 speed = abs(speed)
#
#         if self.moving is True:
#             if direction == self.FORWARD:
#                 self.motor_1.on()
#                 self.motor_2.off()
#                 self.motor_pwm.duty(speed * 10)
#                 self.PID["speed_reqeust"] = speed
#                 self.motor_pid_correct()
#             elif direction == self.BACKWARD:
#                 self.motor_1.off()
#                 self.motor_2.on()
#                 self.motor_pwm.duty(speed * 10)
#
#         # if correct is False:
#             # time.sleep_ms(100)
#             # self.plen = abs(self.pulse.result_p10)
#
#     def stop(self):
#         self.moving = False
#         self.motor_1.off()
#         self.motor_2.off()
#         self.motor_pwm.duty(0)
#
#     def rotary_callback(self, pin):
#         self.debounce_timer.init(period=1, mode=Timer.ONE_SHOT, callback=self.rotary_count_up)
#
#     def rotary_count_up(self, timer):
#         self.PID["count"] += 1
#
#     def get_motor_data(self, timer=None):
#         #                                          delta count                  s -> m      Looptime in s                       steps per rotation
#         self.PID["speed_actual"] = ((self.PID["count"] - self.PID["countOld"]) * (60 * (1000 / self.PID["LOOPTIME"]))) / self.config["motor"]["stepsPerRotation"]
#         self.PID["countOld"] = self.PID["count"]
#
#     def update_pid(self, command, targetValue, currentValue):
#         self.PID["error"] = abs(targetValue) - abs(currentValue)
#         self.PID["pid_result"] = (self.config["motor"]["Kp"] * self.PID["error"]) + (self.config["motor"]["Kd"] * (self.PID["error"] - self.PID["last_error"]))
#         self.PID["last_error"] = self.PID["error"]
#         return constrain(command + int(self.PID["pid_result"]), 0, 1024)  # 255
#
#     def motor_pid_correct(self, timer=None):
#         self.get_motor_data()
#         self.PID["PWM_val"] = self.update_pid(self.PID["PWM_val"], self.PID["speed_request"], self.PID["speed_actual"])
#         self.motor_pwm.duty(self.PID["PWM_val"])
#
#     def deinit(self):
#         self.pid_timer.deinit()


class MotorI2C(object):

    set_speed = const(0x00)
    set_direc = const(0x01)

    direc_stop = const(0x00)
    direc_backward = const(0x01)
    direc_forward = const(0x02)
    direc_off = const(0x03)

    offset_motor_1 = const(0x30)
    offset_motor_2 = const(0x35)

    def __init__(self, i2c, addr, offset=offset_motor_1):
        self.i2c = i2c
        self.addr = addr
        self.offset = offset

        self.currentSpeed = 0
        self.currentDirec = self.direc_stop

        self.i2c.writeto_mem(self.addr, self.offset + self.set_speed, int(0).to_bytes(1, "big"))
        self.i2c.writeto_mem(self.addr, self.offset + self.set_direc, self.direc_stop.to_bytes(1, "big"))

    def move(self, speed=0, direction=-1):
        constrain(speed, -50, 50)

        if direction == -1:
            if speed < 0:
                direction = self.direc_backward
            elif speed == 0:
                direction = self.direc_stop
            elif speed > 0:
                direction = self.direc_forward
        elif direction == self.direc_stop:
            speed = 255
        elif direction == self.direc_off:
            speed = 0

        speed = abs(speed)

        if self.currentDirec != direction:
            # print(direction)
            self.i2c.writeto_mem(self.addr, self.offset + self.set_direc, direction.to_bytes(1, "big"))
        if self.currentSpeed != speed:
            # print(speed)
            self.i2c.writeto_mem(self.addr, self.offset + self.set_speed, int(speed).to_bytes(1, "big"))

        self.currentSpeed = speed
        self.currentDirec = direction

    def stop(self):
        self.move(0, self.direc_stop)

    def off(self):
        self.move(0, self.direc_off)


class DualMI2C:
    def __init__(self, ml: MotorI2C, mr: MotorI2C):
        self.ml = ml
        self.mr = mr

    def move(self, l_speed, r_speed):
        self.ml.move(l_speed)
        self.mr.move(r_speed)

    def stop(self):
        self.mr.stop()
        self.ml.stop()

    def off(self):
        self.mr.off()
        self.ml.off()
