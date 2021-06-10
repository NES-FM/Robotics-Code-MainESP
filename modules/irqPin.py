from machine import *


class IrqPin:
    def __init__(self, pin: int, handler, mode: int = Pin.IN, pull: int = Pin.PULL_UP, trigger: int = Pin.IRQ_FALLING,
                 debounce: int = 150):
        self.pin = pin
        self.mode = mode
        self.pull = pull
        self.handler = handler
        self.trigger = trigger
        self.debounce = debounce

        self.init()

    def init(self):
        self.irq_pin = Pin(self.pin, mode=self.mode, pull=self.pull, handler=self.handler, trigger=self.trigger,
                           debounce=self.debounce)

    def deinit(self):
        self.irq_pin.init(self.pin, mode=self.mode, pull=self.pull, trigger=Pin.IRQ_DISABLE)

    def value(self):
        return self.irq_pin.value()

    def irq_value(self):
        return self.irq_pin.irqvalue()
