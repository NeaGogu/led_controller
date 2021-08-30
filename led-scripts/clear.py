import time
from rpi_ws281x import *
import argparse

import argparse, json

# LED strip configuration:

parser = argparse.ArgumentParser()
parser.add_argument("body")
args = parser.parse_args()
body = json.loads(args.body)


LED_COUNT = 230     # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = body.get("brightness")   # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def clear(strip):
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, 0)
  strip.show()



if __name__ == "__main__":
  strip = Adafruit_NeoPixel(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()
  clear(strip)
