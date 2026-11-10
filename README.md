# Lab 3 实验仓库

## 仓库结构

```
.
├── attack              # 二进制目录
│   ├── dark-calc
│   ├── dark-calc-nx
│   ├── dark-log
│   └── malware
├── payload_canary.py
├── payload_dark.py
├── payload.py
├── payload_rop.py
├── README.md
└── src                 # 部分源码目录，仅供参考
    ├── aslr.c
    ├── dark-calc.c
    └── dark-log.c
```

除了上述文件之外，提交时在根目录中还应当有一份 PDF 格式的实验报告。

所有任务需要使用的二进制都在 `attack` 中，大家不需要自行编译。给大家提供的源码仅包含核心逻辑。

## 任务列表

以下内容需要包含在实验报告当中：

- 任务：观察栈帧 `input` (20 pts 报告)
- 用不同长度的字符串输入测试 `dark-calc` (5 pts 报告)
- 任务：利用缓冲区漏洞执行 `./malware` (25 pts 测试 + 5 pts 报告)
- 用 GDB 检查 main 函数的机器码 (5 pts 报告)
- 任务：栈空间执行 (25 pts 测试 + 5 pts 报告)
- 任务：ROP (10 pts 测试 + 10 pts 报告)
- 任务：Canary (10 pts 测试 + 10 pts 报告)

共 130 分。即使没有通过测试，也需要在报告当中记录自己的想法和尝试，你依然可以拿满报告分数。

本实验中所有报告都会被批改。

## 分数比重

本实验共占课程总分数 13 / 100 分。
