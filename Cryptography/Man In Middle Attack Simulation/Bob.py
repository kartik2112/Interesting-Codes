import socket
import thread
import time
import sys
import subsCipher1411113 as scEnc
import random


print "\n\nHi! This is ---------- Bob's Machine -----------\n\n"
print "I am attempting to connect to Adam and receive his some spicy secret messages :-P\n\n"

prvtKey = random.randint(10,1000)
#prvtKey = 31

p,q = 231, 237

print "p = " + str(p) + ", q = " + str(q)
print "Private Key: " + str(prvtKey) +"\n"

def receiverThread(c,key):
    while True:
        #data = c.recv(1024).decode('utf-8')
        data = c.recv(1024)
        decData = scEnc.decryptThis(data,key)
        if decData == "quit":
            sys.exit(0)
        #print("\r",data,"Eve: ")
        print "\rAdam: " + decData + "\t( Actual message received: "+ data +" )" +"\nBob: ",

s = socket.socket()
print "Bob Server Socket created" 

port = int(input("Enter port for Bob: "))

s.bind(('',port))

print "Bob Server Socket binded to",port

s.listen(5)
print "Bob Server Socket is listening"

c, addr = s.accept()
print "Bob received connection from Adam:",addr


# Share keys
R1 = q**prvtKey % p
print "R1 calculated by Bob's machine: " + str(R1)
c.send(str(R1))
R2 = c.recv(1024)
print "R2 received from Adam's machine: " + R2
R2=int(R2)
print "Calculating key ..."
key = R2**prvtKey % p
print "Handshake complete!\nKey that has been calculated is: " + str(key)



time.sleep(2)
# Start Sharing messages
thread.start_new_thread(receiverThread,(c,key))

while True:
    message = raw_input("Bob: ")    
    encMsg = scEnc.encryptThis(message,key)
    #c.send(message.encode('utf-8'))
    print "\tEncrypted Message Sent: "+encMsg
    c.send(encMsg)
    if message == "quit":
        sys.exit(0)
        
c.close()
