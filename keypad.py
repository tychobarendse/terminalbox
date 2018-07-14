import CHIP_IO.GPIO as GPIO
#key pad----------------------
keypin1 = "LCD-VSYNC"
keypin2 = "LCD-CLK"
keypin3 = "LCD-D22"
keypin4 = "LCD-D20"
keypin5 = "LCD-D18"
keypin6 = "LCD-D14"
keypin7 = "LCD-D12"
keypin8 = "LCD-D10"

key = 0
keycomp1 = 0
keycomp2 = 0    
flag = False

def Setup():
 GPIO.setup(keypin1, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(keypin2, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(keypin3, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(keypin4, GPIO.IN, GPIO.PUD_DOWN)
 GPIO.setup(keypin5, GPIO.OUT, initial=1)
 GPIO.setup(keypin6, GPIO.OUT, initial=1)
 GPIO.setup(keypin7, GPIO.OUT, initial=1)
 GPIO.setup(keypin8, GPIO.OUT, initial=1)		
 print "key setup done......" 
input = [keypin1, keypin2, keypin3, keypin4]
output= [keypin5, keypin6, keypin7, keypin8]

def Get():
	global flag
	global keycomp1
	global keycomp2
	global key
	global doubler
	key = 0

	for y in range(4):
		GPIO.output(output[y], GPIO.LOW)
		for x in range(4):
			if GPIO.input(input[x]) == 0:
#				print ("key", x, y)
				key = ((x+1) + (y*4))
#				print ("key ",key)			
		GPIO.output(output[y],GPIO.HIGH)
	if flag == False:
		keycomp1 = key
		flag = True
	elif flag == True:
		keycomp2 = key
		flag = False

	if keycomp1 != keycomp2 and key != 0:
		return key

Setup()
#while True:
#	print Get()

