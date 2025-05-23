# /*****************************************************************************
# * | File        :	  config.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2020-12-12
# * | Info        :   
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import os
import sys
import time

class RaspberryPi:
    # Pin definition
    RST_PIN     = 18
    CS_PIN      = 22
    DRDY_PIN    = 17

    def __init__(self):
    # SPI device, bus = 0, device = 0
        import spidev
        #import RPi.GPIO
        import gpiozero
        
        #self.GPIO = RPi.GPIO
        self.LED = gpiozero.LED
        self.BUTTON = gpiozero.Button
        self.SPI = spidev.SpiDev(0, 0)

        self.rst_pin = None
        self.cs_pin = None
        self.drdy_pin = None

    def digital_write(self, pin, value):
        #self.GPIO.output(pin, value)
        self.LED(pin, initial_value=value)

    def digital_read(self, pin):
        #return self.GPIO.input(pin)
        return self.LED(pin).value

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.SPI.writebytes(data)
        
    def spi_readbytes(self, reg):
        return self.SPI.readbytes(reg)
        
    def module_init(self):
        #self.GPIO.setmode(self.GPIO.BCM)
        #self.GPIO.setwarnings(False)
        #self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        #self.GPIO.setup(self.CS_PIN, self.GPIO.OUT)
        self.rst_pin = self.LED(self.RST_PIN)
        self.cs_pin = self.LED(self.CS_PIN)
        
        #self.GPIO.setup(self.DRDY_PIN, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        self.drdy_pin = self.BUTTON(self.DRDY_PIN, pull_up=True)
        self.SPI.max_speed_hz = 2000000
        self.SPI.mode = 0b01
        return 0;

    def module_exit(self):
        self.SPI.close()
        #self.GPIO.output(self.RST_PIN, 0)
        #self.GPIO.output(self.CS_PIN, 0)
        self.rst_pin.close()
        self.cs_pin.close()
        self.drdy_pin.close()
        #self.GPIO.cleanup()
        
        
class JetsonNano:
    # Pin definition
    RST_PIN         = 18
    CS_PIN          = 22
    DRDY_PIN        = 17

    def __init__(self):
        import spidev
        self.SPI = spidev.SpiDev(0, 0)
        
        import Jetson.GPIO
        self.GPIO = Jetson.GPIO

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.SPI.writebytes(data)
        
    def spi_readbytes(self, reg):
        return self.SPI.readbytes(reg)

    def module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.CS_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.DRDY_PIN, self.GPIO.IN)
        self.SPI.max_speed_hz = 2000000
        self.SPI.mode = 0b01
        return 0

    def module_exit(self):
        self.SPI.close()
        self.GPIO.output(self.RST_PIN, 0)

        self.GPIO.cleanup()
        
hostname = os.popen("uname -n").read().strip()
        
#if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
#if hostname == "raspberrypi":
if True:
    implementation = RaspberryPi()
else:
    implementation = JetsonNano()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))
