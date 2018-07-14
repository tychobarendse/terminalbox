import CHIP_IO.GPIO as GPIO
from axp209 import AXP209
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import os.path
from luma.core.render import canvas
from PIL import ImageFont, ImageDraw
import serial
import time
import keypad as key
import nmcli
key.Setup()

Oled = i2c(port=1, address=0x3C)
device = ssd1306(Oled)

button = 0
GPSstream = [''] 
while True:
	button = key.Get()
	with canvas(device) as draw:
				dataGPS = open("dataGPS.dat","r+")
				GPSdata = dataGPS.readlines()
				dataGPS.close()
				if len(GPSdata) > 0:
					GPSstream = GPSdata

				button=key.Get()
				font = ImageFont.truetype("FreePixel.ttf", 12) #48 is a great size	
                		draw.text((0, 0), str(GPSstream), fill="white", font=font)
				#draw.text((0, 8), GPSdata[1], fill="white", font=font)
                                #draw.text((0, 16), GPSdata[2], fill="white", font=font)
                                #draw.text((0, 24), GPSdata[3], fill="white", font=font)
                                #draw.text((0, 32), GPSdata[4], fill="white", font=font)
                                #draw.text((0, 40), str(button), fill="white", font=font)
