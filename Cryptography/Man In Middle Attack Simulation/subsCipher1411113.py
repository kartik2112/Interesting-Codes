def encryptThis(str,K):
	s1=list(str)
	
	for i in range(0,len(s1)):
		if s1[i] != ' ':
			s1[i]=chr((ord(s1[i])-ord(' ')+K)%(ord('~')-ord(' ')+1) + ord(' '))
			#s1[i]=chr((ord(s1[i])+K)%128)

	return "".join(s1)

def decryptThis(str,K):
	s1=list(str)

	for i in range(0,len(s1)):
		if s1[i] != ' ':
			s1[i]=chr((ord(s1[i])-ord(' ')-K)%(ord('~')-ord(' ')+1) + ord(' '))
			#s1[i]=chr((ord(s1[i])-K)%128)

	return "".join(s1)
