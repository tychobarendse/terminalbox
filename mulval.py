from multiprocessing import Process, Value, Array
import time
def f(n):#, a):
   s = 0
   while True:
	 n.value = 1
	 time.sleep(1)
	 s += 1
#    for i in range(len(a)):
#        a[i] = -a[i] 

if __name__ == '__main__':
    num = Value('d', 0.0)
#    arr = Array('i', range(10))
    p = Process(target=f, args=(num, ))#arr))
    p.start()
    p.join()
    while True:
	    print num.value
	    time.sleep(2)
#    print arr[:]
