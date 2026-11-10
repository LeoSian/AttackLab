#include <stdio.h>
#include <string.h>

extern char *gets(char *buf);

void grade_eval(int grade) {
  if (grade == 4) printf("\n\033[31m Hope %c will be your grade! \n", 4 - grade + 'A');
  fflush(stdout);
  return;
}

struct log_frame {
  char expression[128]; 
  char logMsg[128];
  int len;
  char pad[8];
};

void input(void) {
  struct log_frame f;

  f.len = 0;
  puts("Enter a log message:");
  if (gets(f.expression) == NULL) return;
  memcpy(f.logMsg + f.len, f.expression, sizeof(f.expression));

  return;
}

int main(void) {
  input();
  puts("Log saved.");
  return 0;
}
