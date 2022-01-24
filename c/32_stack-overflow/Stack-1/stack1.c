#include<stdio.h>

int main()
{
  char buf[100];
  int change_me = 49;
  setvbuf(stdin, 0, 2, 0);
  setvbuf(stdout, 0, 2, 0);
  printf("I dare you to change the value %d\n", change_me);
  gets(buf);
  if (change_me == 50)
  {
    printf("You changed me!!, here's have this gift\n");
    system("/bin/bash");
  }
  else
  {
    printf("You can't change me\n");
  }
  return 0;
}
