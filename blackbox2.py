import CHIP_IO.GPIO as GPIO
from axp209 import AXP209
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import os.path
from luma.core.render import canvas
from PIL import ImageFont, ImageDraw
import serial
#import time
import keypad as key
import nmcli
#from ESPSSD import Screen

screen = 0
databox =[]
def readlimbo():
	global databox
	for i in range(0, len(databox)):
		databox.pop()
	filename = "dataGPS.dat"
	file = open(filename, "r")
	for line in file:
	       databox.append(line,)
	for i in range(0, len(databox)):
        	x = list(databox[i])
        	x.pop()
       	databox[i] = ''.join(x)
	box = databox	

Oled = i2c(port=1, address=0x3C)
device = ssd1306(Oled)

while True:
		readlimbo()
		button = key.Get()
        	with canvas(device) as draw:
			if button == 16:
				screen += 1
			if screen > 5:
				screen = 0

				
			if screen == 0:
				font = ImageFont.truetype("FreePixel.ttf", 48) #48 is a great size
                		draw.text((0, 8), databox[1], fill="white", font=font)
			
				font = ImageFont.truetype("FreePixel.ttf", 8)
                       		draw.text((0, 0), databox[2], fill="white", font=font)
	                	draw.text((56, 0), str(button), fill="white", font=font)
                        	draw.text((74, 0), databox[3], fill="white", font=font)
			
                        	font = ImageFont.truetype("FreePixel.ttf", 16)
                        	draw.text((64, 51), databox[0], fill="white", font=font)
                        	draw.text((0, 51), databox[9], fill="white", font=font)
                        	draw.text((40, 51), databox[5], fill="white", font=font)
			
			elif screen == 1:
		                font = ImageFont.truetype("FreePixel.ttf", 10)
                                draw.text((0, 0), "*SETUP*", fill="white", font=font)
                                draw.text((0, 12), "1. toggle GPS ", fill="white", font=font)
                                draw.text((0, 20), "2. >>", fill="white", font=font)
                                draw.text((0, 28), "3. >>", fill="white", font=font)
                                draw.text((0, 36), "4. >>", fill="white", font=font)
                                draw.text((0, 44), "Setup >>", fill="white", font=font)
                                draw.text((0, 52), "Setup >>", fill="white", font=font)
			
			elif screen == 2:
				font = ImageFont.truetype("FreePixel.ttf", 10)
                                draw.text((0, 0), "axp209", fill="white", font=font)
			
			elif screen == 3:
                                font = ImageFont.truetype("FreePixel.ttf", 10)
                                draw.text((0, 0), "MQ-135", fill="white", font=font)
			elif screen == 4:
                                font = ImageFont.truetype("FreePixel.ttf", 10)
                                draw.text((0, 0), "DH11", fill="white", font=font)

			elif screen == 5:
                                font = ImageFont.truetype("FreePixel.ttf", 10)
                                draw.text((0, 0), "Noice", fill="white", font=font)

