
filename = "dataGPS.dat"
file = open(filename, "r")
GPS =[]
for line in file:
	GPS.append(line,)
print GPS

for i in range(0, len(GPS)):
	x = list(GPS[i])
	x.pop()
	GPS[i] = ''.join(x)

print GPS
