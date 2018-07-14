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

#enableGPS = "XIO-P0"
#GPIO.setup(enableGPS, GPIO.OUT, initial=1)
#GPIO.output(enableGPS, GPIO.LOW) #pull GND pin NEO-6M down to enable module 
#print "GPS enabled............."
#time.sleep(2)

Oled = i2c(port=1, address=0x3C)
device = ssd1306(Oled)

GPGLL = "" #Geographic Position, Latitude / Longitude and time
GPRMC = "" #Recommended minimum specific GPS/Transit data
GPVTG = "" #Track made good and ground speed
GPGGA = "" #Global Positioning System Fix Data
GPGSA = "" #GPS DOP and active satellites
GPGSV = "" #GPS Satellites in view
timeZone = 1
speed = "0"
Latitude =  "XXXXXXXXXXXX"
Longitude = "XXXXXXXXXXXXX"
utc = "XX:XX:XX"
fix = "0"
button = 0
screen = 1
tester = 0
voltageOled = "0"
percOled = "0"
tempOled = "0"
voltOled = "0"
disOLed = "0"
charOled = "0"


def battery():
		global voltageOled
		global percOled
		global voltOled
		global disOled
		global charOled

		axp = AXP209()
		voltage = axp.battery_voltage
                gauge = axp.battery_gauge
		voltage = str("%.1f" % (voltage / 1000))
		buffer = [str(gauge),"%"]
		voltageOled = str("".join(buffer))
		percOled = voltageOled
		temp = axp.internal_temperature
        	buffer = [str(temp)," C"]
       		tempOled = str("".join(buffer))

        	volt = axp.battery_voltage
        	buffer = [str(volt)," mV"]
        	voltOled = str("".join(buffer))

        	discur = axp.battery_discharge_current
       	 	buffer = [str(discur)," Ma discharge"]
        	disOled = str("".join(buffer))

        	charge = axp.battery_charge_current
        	buffer = [str(charge)," Ma charge"]
        	charOled = str("".join(buffer))
		axp.close()
while True:
	button = key.Get()
	with canvas(device) as draw:
			if button == 16:
				screen += 1
				time.sleep(1)
			if screen > 2:
				screen = 1

				
			if screen == 0:
				button=key.Get()
				font = ImageFont.truetype("FreePixel.ttf", 48) #48 is a great size
                		draw.text((0, 8), speedOled, fill="white", font=font)
			
				font = ImageFont.truetype("FreePixel.ttf", 8)
                       		draw.text((0, 0), latitudeOled, fill="white", font=font)
	                	draw.text((56, 0), str(button), fill="white", font=font)
                        	draw.text((74, 0), longitudeOled, fill="white", font=font)
			
                        	font = ImageFont.truetype("FreePixel.ttf", 16)
                        	draw.text((64, 51), timeOled, fill="white", font=font)
                        	draw.text((0, 51), voltageOled, fill="white", font=font)
                        	draw.text((40, 51), fixOled, fill="white", font=font)
			
			elif screen == 1:
				button = key.Get()
				battery()	
				font = ImageFont.truetype("FreePixel.ttf", 24) #48 is a great size
        			draw.text((0, 0), percOled, fill="white", font=font)
        			draw.text((0, 24), voltOled, fill="white", font=font)
        			font = ImageFont.truetype("FreePixel.ttf", 16) #48 is a great size
        			draw.text((64, 0), tempOled, fill="white", font=font)
        			font = ImageFont.truetype("FreePixel.ttf", 8) #48 is a great size
        			draw.text((0, 48), charOled, fill="white", font=font)
        			draw.text((0, 56), disOled, fill="white", font=font)
			
			elif screen == 2:
				con = nmcli.get('con')
				buffer = [con[1],'\n',con[0]]
				conOled = str( ' '.join(buffer))
                                font = ImageFont.truetype("FreePixel.ttf", 8) #48 is a great size
                                draw.text((0, 0), conOled, fill="white", font=font)
