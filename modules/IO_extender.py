from machine import I2C

class IOextender:
	address = 0b1001001
	def __init__(self, i2c):
		self.i2c = i2c
	def readInputs(self):
		data = bytearray(1)
		data[0] = (self.address << 1) | 0
		self.i2c.begin(5)
		self.i2c.start()
		self.i2c.write_bytes(data)
		self.i2c.read_byte()
		self.i2c.stop()
		res = self.i2c.end()
		print(res)
		return res
