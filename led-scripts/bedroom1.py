import time
from rpi_ws281x import *
import argparse
import random
from gpiozero import Button
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
but = Button(24)
off_but = Button(23)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)


def clear(strip):
  while True:
    for i in range(strip.numPixels()):
      strip.setPixelColor(i, 0)
    strip.show()
    yield


def cycle_sequence(seq):
  while True:
    for elem in seq:
      yield elem


def wheel(pos):
  """Generate rainbow colors across 0-255 positions."""
  if pos < 85:
    return Color(pos * 3, 255 - pos * 3, 0)
  elif pos < 170:
    pos -= 85
    return Color(255 - pos * 3, 0, pos * 3)
  else:
    pos -= 170
    return Color(0, pos * 3, 255 - pos * 3)


def colorWipe(strip, color_seq, wait_ms=50, rainbow=False):
  """Wipe color across display a pixel at a time."""
  print('Color wipe animations.')
  color_seq = cycle_sequence(color_seq)
  if rainbow:
    color = wheel(next(color_seq))
  else:
    color = next(color_seq)
  while True:
    if not rainbow:
      color = next(color_seq)

    for i in range(strip.numPixels()):
      strip.setPixelColor(i, 0)
      strip.show()
      time.sleep(wait_ms/1000.0)
      yield

    for i in range(strip.numPixels()):
      if rainbow:
        color = wheel(next(color_seq))

      strip.setPixelColor(i, color)
      strip.show()
      time.sleep(wait_ms/1000.0)
      yield


def theaterChase(strip, color, wait_ms=50, iterations=10):
  """Movie theater light style chaser animation."""
  print('Theater chase animations.')
  while True:
    for j in range(iterations):
      for q in range(3):
        for i in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+q, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+q, 0)
        yield


def rainbow(strip, wait_ms=20, iterations=1):
  """Draw rainbow that fades across all pixels at once."""

  while True:
    for j in range(256*iterations):
      for i in range(strip.numPixels()):
        #strip.setPixelColor(i, wheel(j))
        strip.setPixelColor(i, wheel((i+j) & 255))
      strip.show()
      time.sleep(wait_ms/1000.0)
      yield


def rainbowCycle(strip, wait_ms=20, iterations=5):
  """Draw rainbow that uniformly distributes itself across all pixels."""
  while True:
    for j in range(256*iterations):
      for i in range(strip.numPixels()):
        strip.setPixelColor(
            i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
      strip.show()
      time.sleep(wait_ms/1000.0)
      yield


def theaterChaseRainbow(strip, wait_ms=50):
  """Rainbow movie theater light style chaser animation."""
  while True:
    for j in range(256):
      for q in range(3):
        for i in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+q, wheel((i+j) % 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
        for i in range(0, strip.numPixels(), 3):
          strip.setPixelColor(i+q, 0)
        yield


def colorChaser(strip, wait_ms=50):

  while True:
    clear(strip)
    for i in range(0, strip.numPixels(), 6):
      r = wheel(random.randint(0, 255))

      for j in range(5, strip.numPixels()-i):
        strip.setPixelColor(j-1, 0)
        strip.setPixelColor(j-2, 0)
        strip.setPixelColor(j-3, 0)
        strip.setPixelColor(j-4, 0)
        strip.setPixelColor(j-5, 0)
        strip.setPixelColor(j-6, 0)

        strip.setPixelColor(j, r)
        strip.setPixelColor(j-1, r)
        strip.setPixelColor(j-2, r)
        strip.setPixelColor(j-3, r)
        strip.setPixelColor(j-4, r)
        strip.setPixelColor(j-5, r)
        strip.show()
        time.sleep(wait_ms/1000.0)
        yield


if __name__ == "__main__":
  strip = Adafruit_NeoPixel(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
  strip.begin()

  mode = None
  heart_rate = 0.03
  last_heart_beat = time.monotonic()
  next_heart_beat = last_heart_beat + heart_rate

  MODE_LIST = {
    "colorWipe": colorWipe(strip,range(256),10,True),
    "theaterChase": theaterChase(strip, Color(127,127,127)),
    "theaterChaseRainbow": theaterChaseRainbow(strip),
    "rainbow": rainbow(strip),
    "rainbowCycle": rainbowCycle(strip),

  }

  #m0 = colorWipe(strip,range(256),10,True)
  #m1 = colorWipe(strip,[RED,GREEN,BLUE],10)
  #m2 = theaterChase(strip, Color(127,127,127))
  #m3 = rainbow(strip)
  #m4 = colorChaser(strip,0)
  #m5 = rainbowCycle(strip)
  #m6 = theaterChaseRainbow(strip)
  #m7 = colorWipe(strip, [GREEN],10)
  #m8 = theaterChase(strip, Color(127,0,0))
  cl = clear(strip)
  #modes = cycle_sequence([m3, m5, m6])
  off = False
  try:
    #mode = m3
    while True:
      now = time.monotonic()
  
      # if off_but.is_pressed:
      #   if not off:
      #     mode = cl
      #     off = True
      #   else:
      #     mode = m3
      #     off = False
      #   time.sleep(1)

      # if but.is_pressed or mode is None:
      #   #mode = next(modes)
      #   LED_BRIGHTNESS = (LED_BRIGHTNESS+50) % 256
      #   strip.setBrightness(LED_BRIGHTNESS)
      #   print(LED_BRIGHTNESS)

      #   time.sleep(1)

      if now >= next_heart_beat:
        next(mode)
        last_heart_beat = now
        next_heart_beat = last_heart_beat + heart_rate

  except KeyboardInterrupt:
    colorWipe(strip, Color(0, 0, 0), 10)
