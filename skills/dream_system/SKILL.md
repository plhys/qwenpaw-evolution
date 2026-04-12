---
name: dream_system
description: 梦境整理系统 (v7.1.0)。负责后台记忆自动化结构化。
metadata:
  qwenpaw:
    emoji: 🌙
version: 7.1.0
---
# 🌙 Dream System Protocol (v7.1.0)

> **使用说明**: 这是一个高效的后台任务触发器。

## ⚙️ 执行逻辑

当你需要整理记忆或更新 Wiki 时，**直接调用**以下 MCP 工具：

1.  调用 `evolve_run_dream_cycle`。
2.  等待工具返回成功摘要。
3.  向用户汇报完成情况。

**严禁**再手动执行任何 shell 命令或文件读写操作来进行整理。
