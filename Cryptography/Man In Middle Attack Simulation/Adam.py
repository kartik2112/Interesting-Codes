import socket
import thread
import time
import sys
import subsCipher1411113 as scEnc
import random

print "\n\nHi! This is ---------- Adam's Machine -----------\n\n"
print "I am attempting to connect to Bob and send him some spicy secret messages :-P\n\n"

prvtKey = random.randint(10,1000)
#prvtKey = 53

p,q = 231, 237

print "p = " + str(p) + ", q = " + str(q)
print "Private Key: " + str(prvtKey) +"\n"


def receiverThread(s,key):
    while True:
        #data = s.recv(1024).decode('utf-8')
        data = s.recv(1024)
        decData = scEnc.decryptThis(data,key)
        if decData == "quit":
            sys.exit(0)
        print "\rBob: " + decData + "\t( Actual message received: "+ data +" )" +"\nAdam: ",

s = socket.socket()
port = int(input("Enter port to connect to: "))

s.connect(('127.0.0.1',port))

# Share keys
R1 = q**prvtKey % p
print "R1 calculated by Adam's machine: " + str(R1)
s.send(str(R1))
R2 = s.recv(1024)
print "R2 received from Bob's machine: " + R2
R2=int(R2)
print "Calculating key ..."
key = R2**prvtKey % p
print "Handshake complete!\nKey that has been calculated is: " + str(key)


time.sleep(2)
# Start Sharing messages
thread.start_new_thread(receiverThread,(s,key))

while True:
    message=raw_input("Adam: ")
    encMsg = scEnc.encryptThis(message,key)
    print "\tEncrypted Message Sent: "+encMsg
    s.send(encMsg)
    if message == "quit":
        sys.exit(0)

s.close()