#include <jni.h>
#include "NativeDemo.h"
JNIEXPORT jint JNICALL Java_NativeDemo_factorial
  (JNIEnv *, jobject, jint no){
	int prod=1;
	while(no>0){
		prod*=no;
		no--;
	}
	return prod;
}
