import subprocess
app=subprocess.check_output(['nmcli','device','wifi','list'])
con=subprocess.check_output(['nmcli', 'c', 'show', '--active'])

data4=[]

def trans(data):
	data2=[]
	data3=[]
	sbuffer=''

	for i in range(len(data)):
		data2.append(data[i])

	for x in range(len(data2)):
		if data2[x] != ' ' or data2[x+1] != ' ':
			sbuffer += data2[x]
		else:
			data3.append(sbuffer)
			sbuffer=''

	for i  in range(data3.count('')):
		data3.remove('')
	return data3

def headcut(head):
	for i in range(8,(len(head)-7)):
		data4.append(head[i])

def appoint():
	global data4
	x =[]
	e = data4.index(' Infra')
	for i in range(e-1, e+6):
		x.append(data4[i])
	data4.pop(e)
	return x

def tester():
	k = trans(app)
	headcut(k)
	
	c = data4.count(' Infra')
	print "access point: {}".format(c)
	print "--------------------------------"
	for i in range(c):
		w = appoint()
		print "app: {} pwr: {}".format(w[0], w[4])

	h = trans(con)
	z =''
	for i in range(9, len(h[3])-1):
		z += h[3][i]
	print'----------------------------------'
	print 'Connected ap: {} device: {}'.format(z, h[6])


def get(info):
	global data4
	data4[:]
	getx =[]
	if info == 'app':
		read=subprocess.check_output(['nmcli','device','wifi','list']) 		
		gett = trans(read)
		headcut(gett)

		getc = data4.count(' Infra')
		getx.append(getc)
		for i in range(getc):
			getw = appoint()
			getx.append(getw[0])
			getx.append(getw[4])
		return getx

	elif info == 'con':
		read=subprocess.check_output(['nmcli', 'c', 'show', '--active'])	
		geth = trans(read)
		getz =''
		for i in range(9, len(geth[3])-1):
			getz += geth[3][i]
		getx.append(getz)
		getx.append(geth[6])
		return getx 		

	else:
		print"choose app or con....."
