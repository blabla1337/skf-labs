#include<stdio.h>

int main()
{
	char buf[30];
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	printf("Address: %p\n", &buf);
	printf("Echo: ");
	scanf("%s", &buf);
	printf("You said: %s\n", buf);
	return 0;
}
