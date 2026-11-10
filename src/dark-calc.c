#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <unistd.h>

#define MAXLEN 15

extern char* gets(char *buf);

const char wrapper_front[] = "echo $((";
const char wrapper_back[] = "))";

const char answer[] = "42_is_The_Ànswer";

char command_buf[MAXLEN+16];

void input() {
  char expression[MAXLEN+1];
  printf("Enter an expression (length up to %d):\n", MAXLEN);
  if(!gets(expression) || strlen(expression) == 0) {
      puts(answer);
      exit(0);
  }
  strcpy(command_buf, expression);
}

void eval() {
  int len = strlen(command_buf) > MAXLEN ? MAXLEN : strlen(command_buf);

  memmove(command_buf + 8, command_buf, len+1);
  memcpy(command_buf, wrapper_front, 8);
  strcpy(command_buf + 8 + len, wrapper_back);

  printf("Executing: %s\n", command_buf);
  system(command_buf);

  fflush(stdout);
  return;
}

void grade_eval(int grade) {
  if(grade == 4) printf("\n\033[31m Hope %c will be your grade! \n", 4 - grade + 'A');
  fflush(stdout);
  return;
}

int main(void) {
  while(1){
    input();
    eval();
  }
  return 0;
}
