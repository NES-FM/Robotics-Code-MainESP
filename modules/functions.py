from machine import ADC
from time import sleep_ms
import network


def maprange(list_bounds_1, list_bounds_2, value):
    (a1, a2), (b1, b2) = list_bounds_1, list_bounds_2
    return b1 + ((value - a1) * (b2 - b1) / (a2 - a1))


def debug(a=-1, b=-1, c=-1, d=-1, e=-1, f=-1, g=-1, h=-1, i=-1, j=-1, k=-1, l=-1, m=-1):
    print("LEFT: R: {}, G: {}, B: {} ; C: {} -> {}| RIGHT: R: {}, G: {}, B: {} ; C: {} -> {}| LDR1: {}, LDR2: {} | NP: {}".format(a, b, c, d, e, f, g, h, i, j, k, l, m))
    # print("LDR1: {}, LDR2: {} | NP: {}".format(k, l, m))


def execute(pgm: str):
    try:
        if not (len(pgm.split(".")) > 1 and pgm.split(".")[-1] in "py"):
            pgm = pgm + ".py"
        exec(open(pgm, "r").read(), globals())
    except Exception as e:
        raise e


def constrain(value, lower, upper):
    if value < lower:
        value = lower
    elif value > upper:
        value = upper
    return value


def average_analog_sensor(sensor: ADC, time: int) -> float:
    vals = 0
    for x in range(time):
        vals += sensor.read()
        sleep_ms(1)
    return vals / time


def cat(name: str):
    print(open(name, "r").read())


def net_restart():
    if network.ftp.status()[0] == -1:
        network.ftp.start()
    if network.telnet.status()[0] == -1:
        network.telnet.start()
