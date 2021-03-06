from axp209 import AXP209
import CHIP_IO.GPIO as GPIO
import serial
import time
import sys
import os
from datetime import datetime
#from ESPSSD import Screen

os.system('clear')
enableGPS = "XIO-P0"
GPIO.setup(enableGPS, GPIO.OUT, initial=1)
GPIO.output(enableGPS, GPIO.LOW) #pull GND pin NEO-6M down to enable module 
print "GPS enabled............."
time.sleep(2)

GPGLL = "0,0,0,0,0,0,0" #Geographic Position, Latitude / Longitude and time
GPRMC = "0,0,0,0,0,0,0" #Recommended minimum specific GPS/Transit data
GPVTG = "0,0,0,0,0,0,0" #Track made good and ground speed
GPGGA = "" #Global Positioning System Fix Data
GPGSA = "0,0,0,0,0,0,0" #GPS DOP and active satellites
GPGSV = "0,0,0,0,0,0,0" #GPS Satellites in view

gauge = 0
speed = "*"
latitude =  "[ NO DATA ]"
longitude = "[ NO DATA ]"
altitude = "**"
ttime = "**:**:**"
fix = "*"
SatT = "*"
SatV = "00"

def Remote():
	DisGauge = str(gauge)
	DisGauge += '%'
	Screen(0, 24 ,'0', 0, DisGauge)

def Bat():
	global gauge
        axp = AXP209()
        gauge = axp.battery_gauge
	axp.close()

def Speed():
	global speed
	speed = ""
#	print GPVTG
	Glist = list(GPVTG)
	end = Glist.index('K') - 1 #len(GPVTG) - 5#11 #9
	start = Glist.index('N') + 2 #end - 5#(len(GPVTG) - 14) - (len(GPVTG) - 35)  #14
	for i in range(start, end):
		speed += str(GPVTG[i])
	return speed

def Latitude():
	global latitude
	latitude = ""
	Glist = list(GPGLL)
	endLat = 19
	startLat = 7	
	for i in range(startLat, endLat):
		latitude += str(GPGLL[i])
	return 	latitude

def Longitude():
        global longitude
	longitude = ""
        endLon = 33
        startLon = 20
        for i in range(startLon, endLon):
                longitude += str(GPGLL[i])
	return longitude

def Fix():
        global fix
	fix = ""
        startFix = 44
        fix += str(GPGGA[startFix])
	return fix

def Time():
	global ttime
	ttime = ""
	startTime = 7
	endTime = startTime + 8
	for i in range(startTime, endTime):
		ttime += str(GPGGA[i])
	return ttime

def Sat():
	global SatV
	SatV = ""
	Glist = list(GPGSV)
	startSat = Glist.index(',') + 5
	endSat = startSat + 2
	for i in range(startSat, endSat):
		SatV += str(GPGSV[i])
	return SatV

def Alt():
	global altitude
	altitude = ""
	ripper = list(GPGGA)
	#Glist = list(GPGGA)

	for i in range(0, 11):
		a = ripper.index(',')
		ripper.pop(a)

	altstar = ripper.index(',')
	altend = ripper.index('M')
	for i in range(altstar, len(ripper)):
		altitude += str(ripper[i])
	return altitude

def Data():
	global GPGGA
	global GPGLL
        global GPGSA
        global GPGSV
        global GPRMC
        global GPVTG

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

        if len(GPVTG) > 34:
		Speed()
        else:
		speed = "*"

        if len(GPGLL) > 29:
                        Latitude()
			Longitude()
        else:
                        latitude =  "[x NODATA x]"
                        longitude = "[x NODATA x]"

        if len(GPGGA) > 10:
                        Time()
        else:
                        time = "$$:$$:$$"

        if len(GPGGA) > 73:
                        Fix()
        else:
                        fix = "0"

	if len(GPGSV) > 0:
			Sat()
	else: 
			SatV = "00" 

	if len(GPGGA) > 60:
			Alt()
	else:
			altitude = "**"

with serial.Serial('/dev/ttyS0', 9600) as ser:
	while True:
	#	print GPVTG
	#	print GPGLL
	#	print GPGSV
	#	print len(GPGSV)
	#	print GPGGA
	#	print len(GPGGA) 
		data = ser.readline()
		Data()
		Bat()
	#	print altitude
		print GPGLL
		print "\r time {}{}:{}{}:{}{} Speed {} Latitude {}  Longitude {} Fix {} sattracked {} satview {} alt {} bat {}%".format(ttime[0], ttime[1], ttime[2], ttime[3], ttime[4], ttime[5], speed, latitude, longitude, fix, SatT, SatV, altitude, gauge)
		dataGPS = open("dataGPS.dat", "w")
		lines = [ttime[0], ttime[1], ttime[2], ttime[3], ttime[4], ttime[5],'\n', speed,'\n', latitude,'\n', longitude,'\n', altitude,'\n', fix,'\n', SatT,'\n', SatV,'\n', altitude,'\n', str(gauge),'\n' ]
		dataGPS.writelines(lines)
#		dataGPS.write(ttime[0])
#		dataGPS.write(ttime[1])
#		dataGPS.write(ttime[2])
#		dataGPS.write(ttime[3])
#		dataGPS.write(ttime[4])
#		dataGPS.write(ttime[5])
#		dataGPS.write("\n")
#		dataGPS.write(speed)
#		dataGPS.write("\n")
#		dataGPS.write(latitude)
#		dataGPS.write("\n")
#		dataGPS.write(longitude)
#		dataGPS.write("\n")
#		dataGPS.write( fix)
#		dataGPS.write("\n")
#		dataGPS.write(altitude)
#		dataGPS.write("\n")
		dataGPS.close()
#		Remote()
		time.sleep(1)
