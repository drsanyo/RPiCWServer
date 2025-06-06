from BusinessLogic.platform_detector import IS_RASPBERRYPI
import busio
import adafruit_si5351
from BusinessLogic.si5351Base import Si5351Base

if IS_RASPBERRYPI:
    import adafruit_blinka.board.raspberrypi.raspi_40pin as board
    BOARD_SCL = board.SCL
    BOARD_SDA = board.SDA


class Si5351(Si5351Base):
    def __init__(self, i2c_bus=1, i2c_address=0x60):
        super().__init__(i2c_bus, i2c_address)
        i2c = busio.I2C(BOARD_SCL, BOARD_SDA)
        self.board = adafruit_si5351.SI5351(i2c)
        self.board.clock_0.enabled = False

    def set_frequency(self, freq_hz):
        # self.board.clock_0.configure_clock(freq_hz, adafruit_si5351.SI5351_PLL_A)
        pass

    def key_on(self):
        self.board.clock_0.enabled = True

    def key_off(self):
        self.board.clock_0.enabled = False