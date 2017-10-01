import socket
import thread
import time
import sys
import subsCipher1411113 as scEnc
import random


print "\n\nHi! This is ---------- Eevveee -----------\n\n"
print "Adam, Bob you guys think you have spicy secret messages? How can such gossip be missed by me!\n\n"

prvtKey = random.randint(10,1000)
#prvtKey = 37

p,q = 231, 237

print "p = " + str(p) + ", q = " + str(q)
print "Private Key: " + str(prvtKey) +"\n"

def receiverThreadAdam(cAdam,keyAdam,sBob,keyBob):
    while True:
        #data = cAdam.recv(1024).decode('utf-8')
        data = cAdam.recv(1024)
        decData = scEnc.decryptThis(data,keyAdam)
        if decData == "quit":
            sys.exit(0)
        #print("\r",data,"Eve: ")
        print "\rAdam: " + decData + "\t( Actual message received: "+ data +" )" +"\nDo you want to change content of this message?(y/n) "
        if raw_input() == "y":
            message = raw_input("Enter message to be sent to Bob: ")
            message = scEnc.encryptThis(message,keyBob)
            print "\tEncrypted message sent to Bob: " + message
            sBob.send(message)
        else:
            sBob.send(scEnc.encryptThis(decData,keyBob))
            

def receiverThreadBob(cAdam,keyAdam,sBob,keyBob):
    while True:
        #data = cAdam.recv(1024).decode('utf-8')
        data = sBob.recv(1024)
        decData = scEnc.decryptThis(data,keyBob)
        if decData == "quit":
            sys.exit(0)
        #print("\r",data,"Eve: ")
        print "\rAdam: " + decData + "\t( Actual message received: "+ data +" )" +"\nDo you want to change content of this message?(y/n) "
        if raw_input() == "y":
            message = raw_input("Enter message to be sent to Adam: ")
            message = scEnc.encryptThis(message,keyAdam)
            print "\tEncrypted message sent to Adam: " + message
            cAdam.send(message)
        else:
            cAdam.send(scEnc.encryptThis(decData,keyAdam))


sBobClient = socket.socket()
sAdamServer = socket.socket()
print "Sockets created" 

portBob = int(input("Enter port that Bob is allowing connectios to: "))
portAdam = int(input("Enter port that Adam is attempting to connect to: "))

sBobClient.connect(('127.0.0.1',portBob))
print "Established connection with Bob"

sAdamServer.bind(('',portAdam))
print "Eve Server Socket binded to",portAdam
sAdamServer.listen(5)

cAdam, addr = sAdamServer.accept()
print "Established connection with Adam:",addr

print "\nLets fool them now!\n"


# Share keys
R1 = q**prvtKey % p
print "R1 calculated by Eve's machine: " + str(R1)

sBobClient.send(str(R1))
print "Sent Bob my R1"
cAdam.send(str(R1))
print "Sent Adam my R1"

R2Bob = sBobClient.recv(1024)
print "\nR2 received from Bob's machine: " + R2Bob
R2Bob=int(R2Bob)
print "Calculating key for communicating with Bob ..."
keyBob = R2Bob**prvtKey % p
print "Handshake complete with Bob!\nKey that has been calculated for communicating with Bob is: " + str(keyBob)

R2Adam = cAdam.recv(1024)
print "\nR2 received from Adam's machine: " + R2Adam
R2Adam=int(R2Adam)
print "Calculating key for communicating with Adam ..."
keyAdam = R2Adam**prvtKey % p
print "Handshake complete with Adam!\nKey that has been calculated for communicating with Adam is: " + str(keyAdam) + "\n"




# Start Sharing messages
thread.start_new_thread(receiverThreadAdam,(cAdam,keyAdam,sBobClient,keyBob))
thread.start_new_thread(receiverThreadBob,(cAdam,keyAdam,sBobClient,keyBob))

# while True:
#     message = raw_input("Bob: ")    
#     encMsg = scEnc.encryptThis(message,key)
#     #c.send(message.encode('utf-8'))
#     print "\tEncrypted Message Sent: "+encMsg
#     c.send(encMsg)
#     if message == "quit":
#         sys.exit(0)
        
# c.close()

time.sleep(1000)
