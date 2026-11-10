#include <stdio.h>

int main() {
  int i = 42;         // This local variable is stored on the stack.
  printf("%p\n", &i); // Print the address of i.
  return 0;
}
