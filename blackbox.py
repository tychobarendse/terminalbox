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
from ESPSSD import Screen
key.Setup()

enableGPS = "XIO-P0"
GPIO.setup(enableGPS, GPIO.OUT, initial=1)
GPIO.output(enableGPS, GPIO.LOW) #pull GND pin NEO-6M down to enable module 
print "GPS enabled............."
time.sleep(2)

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
screen = 0
tester = 0

def Speed():
	global speed
	end = len(GPVTG) - 11 #9
	start = (len(GPVTG) - 14) - (len(GPVTG) - 35)  #14
	for i in range(start, end):
		speed += str(GPVTG[i])
#	print len(GPVTG)

def Location():
	global Latitude
	global Longitude
	endLat = 19
	startLat = 7	
	endLon = 33
	startLon = 20
	for i in range(startLat, endLat):
		Latitude += str(GPGLL[i])
	for i in range(startLon, endLon):
		Longitude += str(GPGLL[i])

def Fix():
	global fix
	startFix = 44
	fix += str(GPGGA[startFix])

def Time():
	global utc
	startTime = 7
	endTime = startTime + 8
	for i in range(startTime, endTime):
		utc += str(GPGGA[i])

with serial.Serial('/dev/ttyS0', 9600) as ser:
	while True:
    		data = ser.readline()
		if data[4] == 'G' and data[5] == 'A':
			GPGGA = data
		elif data[4] == 'L' and data[5] == 'L':
			GPGLL = data
		elif data[4] == 'S' and data[5] == 'A':
			GPGSA = data
		elif data[4] == 'S' and data[5] == 'V':
			GPGSV = data
		elif data[4] == 'M' and data[5] == 'C':
			GPRMC = data
		elif data[4] == 'T' and data[5] == 'G':
			GPVTG = data
		else:
			GPGGA = "0"
			GPGLL = "0"
			GPGSA = "0"
			GPGSV = "0"
			GPRMC = "0"
			GPVTG = "0"

		if len(GPVTG) > 34:
			Speed()
		else:
			speed = "XXXXX"

		if len(GPGLL) > 33:
			Location()
		else:
			Latitude =  "[x NODATA x]"
			Longitude = "[x NODATA x]"	        
		
		if len(GPGGA) > 10:
			Time()
		else:
			utc = "$$:$$:$$"

		if len(GPGGA) > 73:
			Fix()
		else:
			fix = "0"

		buffer = [utc[0],utc[1], ':',utc[2],utc[3],':',utc[4],utc[5]]
		
		timeOled = str("".join(buffer))
		Screen(0,24,'0',0,timeOled)
		utc = ""

		latitudeOled = str(Latitude)
      		Latitude = ""
               	longitudeOled = str(Longitude)
		Longitude = ""
		
		speedOled = str(speed)		
		speed = ""
		
		buffer = ["F", fix]
		fixOled = str("".join(buffer))
		fix = ""

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

		button = key.Get()
        	with canvas(device) as draw:
			if button == 16:
				screen += 1
				#time.sleep(1)
			if screen > 2:
				screen = 0

				
			if screen == 0:
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
