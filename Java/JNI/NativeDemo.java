class NativeDemo{
	native int factorial(int no); /* This is the method that is to be written in other language such as C or C++ */

	static{
		/*
		  This will use libNTVEDEMO.so in linux,
		  libNTVEDEMO.dylib in Mac, NTVEDEMO.dll in Windows
		*/
		System.loadLibrary("NTVEDEMO");
	}

	public static void main(String[] args){
		System.out.println("Factorial of 5="+new NativeDemo().factorial(5)); //Here is the call to this native function
		System.out.println("Factorial of 8="+new NativeDemo().factorial(8));
	}
}
