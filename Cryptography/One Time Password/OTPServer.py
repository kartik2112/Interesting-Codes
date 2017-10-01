import socket
import thread
import sys
import random
import time

def serverThread(client1,clientNo,addr):
    client1.send(str(clientNo))
    print "Sent function No",clientNo," to",addr

    no = random.randint(3,100)
    client1.send(str(no))
    print "Sent random no challenge:",no,"to",addr

    resp = client1.recv(1024)
    if int(resp) == functionValueCompute(clientNo,no):
        client1.send("Auth")
        print "Correct response received. Authorized client",clientNo,"Authenticated"
    else:
        client1.send("NAuth")
        print "Incorrect response received. Unauthorized client found!"

def functionValueCompute(functionNo,no):
    noPrimes = [j for i in range(2,3000) for j in range(2*i,3000,i)]
    primes = [i for i in range(2,3000) if i not in noPrimes]
    if functionNo==1:
        return no*23453%3460
    elif functionNo==2:
        return int(no**0.5)
    else:
        return primes[no]

noC = input("No of client connections awaiting:")

serverS = socket.socket()
port1 = int(input("Enter port for client: "))

serverS.bind(('',port1))
serverS.listen(noC)

for i in range(1,noC+1):
    client1, addr = serverS.accept()

    print "Established connection with Client:",addr
    time.sleep(0.5)
    thread.start_new_thread(serverThread,(client1,i,addr))
