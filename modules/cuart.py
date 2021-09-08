from modules.pins import pins
import machine
import time

def uts(s):
    '''unsigned to signed'''
    if s >= 128:
        return s - 256
    return s


def line_handler(data, thctm_values, config):
    #                       type     angle         midfactor
    thctm_values["line"] = (data[0], uts(data[1]), uts(data[2]))
    if config["debug"]["cuart_time"]:
        last = thctm_values["time"]
        now = time.time()
        print("CUART: Line: {}s since last time".format(round(now-last,3)))
        thctm_values["time"] = now
    if config["debug"]["cuart_data"]:
        print("CUART: Line:", data[0], uts(data[1]), uts(data[2]))
    return data[3:]


def green_handler(data, thctm_values, config):
    values = {k: v for k, v in zip(["tl", "tr", "dl", "dr"], [(data[0] & x) != 0 for x in [CUART.gtype_tl, CUART.gtype_tr, CUART.gtype_dl, CUART.gtype_dr]])}
    thctm_values["green"] = values
    if config["debug"]["cuart_data"]:
        print("CUART: Green:",values)
    return data[1:]


def unknown_packet(data, thctm_values):
    print("CUART: Unknown data:", data)
    return data


handlers = {
    "L": line_handler,
    "G": green_handler
}


class CUART:
    ltype_straight = 0x00
    ltype_90l = 0x01  # 90 degrees left
    ltype_90r = 0x02  # 90 degrees right
    ltype_tl = 0x03  # -|  t with exit left
    ltype_tr = 0x04  # |-  t with exit right
    ltype_t = 0x05  # T    t with exit bottom
    ltype_X = 0x06  # +    4 way crossing
    ltype_space = 0x07 # Line ending -> space incoming
    ltype_unknown = 0x20 # Something went wrong here

    ltype_strings = {ltype_straight: "Straight", ltype_90l: "90 Left", ltype_90r: "90 Right", ltype_tl: "T left", ltype_tr: "T right", ltype_t: "T bottom", ltype_X: "4 Way", ltype_space: "Space", ltype_unknown: "Unknown"}

    gtype_none = 0b0000
    gtype_tl = 0b1000
    gtype_tr = 0b0100
    gtype_dl = 0b0010
    gtype_dr = 0b0001

    def __init__(self, thctm_values, config, uart_num=1, baudrate=115200, bits=8, parity=None, tx=pins["Tx-Cam"],
                        rx=pins["Rx-Cam"], timeout=15, buffer_size=512, lineend=b'\n'):
        self.thctm_values = thctm_values
        self.config = config
        self.uart_num = uart_num
        self.baudrate = baudrate
        self.bits = bits
        self.parity = parity
        self.tx = tx
        self.rx = rx
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.lineend = lineend
        self.uart = machine.UART(uart_num, tx=self.tx, rx=self.rx, baudrate=self.baudrate, bits=self.bits,
                        parity=self.parity, timeout=self.timeout, buffer_size=self.buffer_size, lineend=self.lineend)
        self.uart.callback(machine.UART.CBTYPE_PATTERN, self.callback, pattern=self.lineend)

    def init(self):
        self.uart.init(tx=self.tx, rx=self.rx, baudrate=self.baudrate, bits=self.bits, parity=self.parity,
                                 timeout=self.timeout, buffer_size=self.buffer_size, lineend=self.lineend)

    def callback(self, arg):
        if arg[0] == self.uart_num and arg[1] == 2:
            data = arg[2].encode("UTF-8")
            while len(data) > 0:
                data = handlers.get(chr(data[0]), unknown_packet)(data[1:], self.thctm_values, self.config)
