import socket
import thread
import sys
import time


def functionValueCompute(functionNo,no):
    noPrimes = [j for i in range(2,3000) for j in range(2*i,3000,i)]
    primes = [i for i in range(2,3000) if i not in noPrimes]
    if functionNo==1:
        return no*23453%3460
    elif functionNo==2:
        return int(no**0.5)
    else:
        return primes[no]

s = socket.socket()
port = int(input("Enter port to connect to: "))
#addr = input("Enter IPv4 Address to connect to")
addr = "127.0.0.1"

s.connect((addr,port))

fnNo = s.recv(1024)
print "Function No:",fnNo,"received"

no = s.recv(1024)
print "Challenge no:",no,"received"

#for i in range(0,10):
#    time.sleep(0.5)
#    print "\r -",
#    time.sleep(0.5)
#    print "\r \\",
#    time.sleep(0.5)
#    print "\r |",
#    time.sleep(0.5)
#    print "\r /",


print "\nExpected Response To Be Sent:",functionValueCompute(int(fnNo),int(no))
resp1 = input("Enter response:")
#s.send(str(functionValueCompute(int(fnNo),int(no))))
s.send(str(resp1))

status = s.recv(1024)
if status == "Auth":
    print "Correct response sent! You are authorized!"
else:
    print "Incorrect response sent! You are NOT authorized!!!"



