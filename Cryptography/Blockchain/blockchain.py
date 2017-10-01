import os
import hashlib

chainList = [elem for elem in os.listdir("./BlockChain") if elem.endswith(".txt")]

print("Blocks found:")
print(chainList)

lastHash = ""

blockCount=0

lineCount=0

for elem in chainList:
	blockCount+=1
	latestFile = "./BlockChain/"+elem
	
	blockFile=open("./BlockChain/"+elem,"r")
	header = blockFile.readline()
	
	# print(header)
	
	# https://docs.python.org/2/library/md5.html
	m = hashlib.md5()
	
	if ("00000000000000000000000000000000" not in header):
		print("Not 1st block")
		if (lastHeader in header):
			print("Block " + str(blockCount-1) + " is unmodified. Hash of block " + str(blockCount-1) + ": "+lastHeader.strip())
		else:
			print("Block " + str(blockCount-1) + " has been modified !!!!!!!!! Blockchain has been modified. Cutting off all further transactions !")
			exit(0)
	
	lineCount=0
	blockFile=open("./BlockChain/"+elem,"r")
	for line in blockFile:
		m.update((line+"\n").encode('utf-8'))
		lineCount+=1
		print(line,end='')
	blockFile.close()
	if lineCount <4:
		break
	lastHeader = m.hexdigest()
	print()
	
trns = input("\nEnter transaction of form: 'Sender, Receiver, Amount': ")
if lineCount == 4:
	blockFile = open("./BlockChain/block %04d.txt" % (blockCount+1),"w")
	# print(lastHeader)
	blockFile.write((lastHeader).strip()+"\n")
	blockFile.write(trns+"\n")
else:
	blockFile = open(latestFile,"a")
	blockFile.write(trns+"\n")
