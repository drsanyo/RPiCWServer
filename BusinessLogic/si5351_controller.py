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
        if not (1_000_000 <= freq_hz <= 30_000_000):
            raise ValueError("Frequency must be between 1 MHz and 30 MHz.")

        # Set PLL A to 900 MHz (25 MHz crystal * 36)
        self.board.pll_a.configure_integer(36)

        # Calculate ideal divider
        pll_freq = 900_000_000
        ideal_div = pll_freq / freq_hz
        int_div = int(ideal_div)
        frac = ideal_div - int_div

        # Convert fraction to numerator and denominator
        # We'll use a max denominator of 1,000,000 for ~100 Hz accuracy
        max_denom = 1_000_000
        numerator = round(frac * max_denom)
        denominator = max_denom

        # Reduce fraction
        from math import gcd
        g = gcd(numerator, denominator)
        numerator //= g
        denominator //= g

        # Apply fractional configuration to clock 0
        self.board.clock_0.configure_fractional(self.board.pll_a, int_div, numerator, denominator)
        self.board.outputs_enabled = True

        # Debug
        actual_freq = self.board.clock_0.frequency
        error = abs(actual_freq - freq_hz)
        print(f"Requested: {freq_hz} Hz")
        print(f"Actual:    {actual_freq:.2f} Hz (error: {error:.2f} Hz)")

    def key_on(self):
        self.board.outputs_enabled = True

    def key_off(self):
        self.board.outputs_enabled = False