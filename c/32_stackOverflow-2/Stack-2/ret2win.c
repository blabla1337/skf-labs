#include <stdio.h>

void win()
{
  system("/bin/bash");
}

int main()
{
  char buf[20];
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  printf("Tell me your name: ");
  gets(buf);
  return 0;
}

