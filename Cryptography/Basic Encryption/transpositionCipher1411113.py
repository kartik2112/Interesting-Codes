print("Enter string to be encrypted:",end=' ')
s1=list(input())

print("Enter encryption key:",end=' ')
dec=[0]+[int(n) for n in input().split()]
enc=[0]*len(dec)
for i in range(1,len(dec)):
	enc[dec[i]]=i
s1+=[chr(2)]*(5-len(s1)%5)

print("Encryption Key:",enc[1:])
print("Decryption Key:",dec[1:])
s1Mat=[[]]*(len(s1)//(len(dec)-1))

for i in range(0,len(s1Mat)):
	s1Mat[i]=s1[i*5:(i+1)*5]


encStr=[0]*(len(enc)-1)

for i in range(0,len(enc)-1):
	encStr[enc[i+1]-1]=[]
	for j in range(0,len(s1Mat)):
		encStr[enc[i+1]-1]+=(s1Mat[j][i])

encStrFin=""
for elem in encStr:
	encStrFin+="".join(elem)
print("String after encryption: ",encStrFin.upper())


encStrFin=list(encStrFin)
encStrMat=[0]*(len(encStrFin)//(len(dec)-1))
k=0
for i in range(0,len(encStrMat)):
	encStrMat[i]=[0]*(len(dec)-1)
for i in range(0,len(dec)-1):
	for j in range(0,len(s1Mat)):
		encStrMat[j][i]=encStrFin[k]
		k+=1
		
decStr=[0]*(len(dec)-1)
for i in range(0,len(dec)-1):
	decStr[dec[i+1]-1]=[]
	for j in range(0,len(encStrMat)):
		decStr[dec[i+1]-1]+=(encStrMat[j][i])
#print(decStr)
decStrFin=""
for i in range(0,len(decStr[0])):
	for j in range(0,len(decStr)):
		decStrFin+=decStr[j][i]
print("String after decryption: ",decStrFin)

decStrFin=decStrFin[:decStrFin.find(chr(2))]
print("String after stripping: ",decStrFin)

# Output:

# F:\OneDrive\Academics\KJSCE Stuff\Sem 7\CSS\Practicals\Expt 1 - Ciphering>python transpositionCipher1411113.py
# Enter string to be encrypted: theenemyattackstonight
# Enter encryption key: 3 1 4 5 2
# Encryption Key: [2, 5, 1, 3, 4]
# Decryption Key: [3, 1, 4, 5, 2]
# String after encryption:  EYCNTETTHEAKINTSGHMAOT
# String after decryption:  theenemyattackstonight
# String after stripping:  theenemyattackstonight