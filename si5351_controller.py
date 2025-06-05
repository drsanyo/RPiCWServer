import os

IS_RASPBERRYPI = os.uname()[1] == 'raspberrypi'

class Clock0Mock:
    frequency = 0
    enabled = False

class SMBusMock:
    clock_0 = Clock0Mock()
    clock_1 = Clock0Mock()
    clock_2 = Clock0Mock()
    def __init__(self, addr):
        pass

    def write_byte_data(self, a, b, c):
        pass


class Si5351:
    def __init__(self, i2c_bus=1, i2c_address=0x60):
        if IS_RASPBERRYPI:
            import board
            import busio
            import adafruit_si5351
            i2c = busio.I2C(board.SCL, board.SDA)

            self.bus = adafruit_si5351.SI5351(i2c)
            self.bus.clock_0.enabled = False
        else:
            self.bus = SMBusMock(i2c_bus)


    def set_frequency(self, freq_hz):
        self.bus.clock_0.frequency = freq_hz

    def key_on(self):
        self.bus.clock_0.enabled = True

    def key_off(self):
        self.bus.clock_0.enabled = False