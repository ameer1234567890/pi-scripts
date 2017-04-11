# *-* coding: utf-8 -*-
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import argparse

parser = argparse.ArgumentParser(description='Example with non-optional arguments')
parser.add_argument('downspeed', action="store", type=float)
parser.add_argument('upspeed', action="store", type=float)
results = parser.parse_args()

# Raspberry Pi pin configuration:
RST = 14

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

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 0
shape_width = 20
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
#font = ImageFont.truetype('Minecraftia.ttf', 8)

# Clear display.
disp.clear()

# Write two lines of text.
draw.text((x, top),    'Down Speed: {} Mbps'.format(results.downspeed),  font=font, fill=255)
draw.text((x, top+20), 'Up Speed: {} Mbps'.format(results.upspeed), font=font, fill=255)

# Display image.
disp.image(image)
disp.display()
