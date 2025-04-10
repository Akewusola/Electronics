import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_GPIO.Platform as Platform
Platform.platform_detect = lambda: Platform.RASPBERRY_PI  # Force Pi detection

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

def display_oled(text):
    """Display text on OLED screen"""
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    y = 0
    for line in text.split('\n'):
        draw.text((0, y), line, font=font, fill=255)
        y += 10
    disp.image(image)
    disp.display()

def clear_display():
	disp.clear()
	disp.display()  
