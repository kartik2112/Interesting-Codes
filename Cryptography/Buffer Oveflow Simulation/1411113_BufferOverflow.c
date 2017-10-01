#include <stdio.h>
#include <stdlib.h>
#include<string.h>
int main(){
	char *ptr;
	char *dptr;
	ptr=(char*)malloc(10*sizeof(char));
	dptr=(char*)malloc(10*sizeof(char));
	printf("Address of ptr:%d\n",ptr);
	printf("Address of dptr:%d\n",dptr);
	printf("\n\nEnter the string:");
	gets(ptr);
	
	printf("%s   %s",ptr,dptr);
	system(dptr);
	
	return 0;
}