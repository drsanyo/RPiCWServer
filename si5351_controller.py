import os

IS_RASPBERRYPI = os.uname()[1] == 'raspberrypi'

class ClockMock:
    def __init__(self, frequency, enabled):
        self._frequency = frequency
        self._enabled = enabled

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value
        print('set frequency to ' + str(value))

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        print('set enabled to ' + str(value))

class SMBusMock:
    clock_0 = ClockMock(frequency=0, enabled=False)
    def __init__(self, addr):
        pass

class Si5351:
    def __init__(self, i2c_bus=1, i2c_address=0x60):
        if IS_RASPBERRYPI:
            import board
            import busio
            import adafruit_si5351
            i2c = busio.I2C(board.SCL, board.SDA)

            self.board = adafruit_si5351.SI5351(i2c)
            self.board.clock_0.enabled = False
        else:
            self.board = SMBusMock(i2c_bus)


    def set_frequency(self, freq_hz):
        self.board.clock_0.frequency = freq_hz

    def key_on(self):
        self.board.clock_0.enabled = True

    def key_off(self):
        self.board.clock_0.enabled = False