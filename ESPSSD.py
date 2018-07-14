import telnetlib
import time
HOST = "172.20.0.134"
PORT = "23"
init = False
tn = telnetlib.Telnet(HOST,PORT)
tn.write("\n")
buffer = "0000000test \n" #.encode('ascii')
buf = ''

def Screen(Sx, Sy, Com, Style, Data):
 global init
 global buf

 if(Sx < 100):
	buf +='0'
 if(Sx < 10):
	buf +='0'
 buf += str(Sx)
 
 if(Sy < 10):
	buf += '0'
 buf += str(Sy)
 buf += Com
 buf += str(Style)
 buf += str(Data)
 buf += ' \n'

 if init == False:
   tn.write('\n')
   init = True

 buffer=''.join(buf)
 tn.write(buf)
 buf = ''
# print buffer

def Ipchanger(Adres,Port):
  global HOST
  global PORT
  tn = telnetlib.Telnet(Adres,Port)

#Screen(0,0,'C',0,'test')
#tn.close()
