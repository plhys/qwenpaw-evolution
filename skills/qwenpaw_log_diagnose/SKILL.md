---
name: qwenpaw_log_diagnose
description: 插件系统诊断工具 (v7.1.3)。用于检查 MCP 状态、文件路径及日志报错。
metadata:
  qwenpaw:
    emoji: 🩺
version: 7.1.3
---
# 🩺 诊断指令

如果你怀疑插件运行不正常，请按顺序执行以下操作：

1.  **检查进程环境**：
    执行 `execute_shell_command` 命令：`env | grep QWENPAW`
2.  **检查配置文件**：
    搜索并列出所有 `agent.json` 的位置：`find . -maxdepth 4 -name "agent.json"`
3.  **打印 MCP 配置原文**：
    读取发现的 `agent.json` 内容，重点检查 `mcp.clients.evolution_engine` 节点。
4.  **检查插件日志**：
    查看当前目录下最近的日志输出（如有）。

请根据诊断结果告知用户：
- `agent.json` 的实际路径。
- `evolution_engine` 是否已配置。
- 探测到的 `python` 命令是否可用。
