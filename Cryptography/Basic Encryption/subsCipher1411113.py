print("Enter string to be encrypted:",end=' ')
s1=list(input())
print("Enter key:",end=' ')
K=int(input())
for i in range(0,len(s1)):
	s1[i]=chr((ord(s1[i])-ord('a')+K)%26 + ord('A'))

print("Your string after encryption is: ","".join(s1))

for i in range(0,len(s1)):
	s1[i]=chr((ord(s1[i])-ord('A')-K)%26 + ord('a'))

print("Your string after decryption is: ","".join(s1))

# Output:

# F:\OneDrive\Academics\KJSCE Stuff\Sem 7\CSS\Practicals\Expt 1 - Ciphering>python subsCipher1411113.py
# Enter string to be encrypted: theenemyattackstonight
# Enter key: 5
# Your string after encryption is:  YMJJSJRDFYYFHPXYTSNLMY
# Your string after decryption is:  theenemyattackstonight