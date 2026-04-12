# QwenPaw Evolution

> **QwenPaw 自我进化引擎** — v7.1.8

[![GitHub stars](https://img.shields.io/github/stars/plhys/qwenpaw-evolution)](https://github.com/plhys/qwenpaw-evolution/stargazers)
[![GitHub license](https://img.shields.io/github/license/plhys/qwenpaw-evolution)](https://github.com/plhys/qwenpaw-evolution/blob/main/LICENSE)
[![Python version](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![QwenPaw version](https://img.shields.io/badge/QwenPaw-1.1.0+-green)](https://github.com/QwenPawTeam/qwenpaw)

**QwenPaw Evolution** 将 QwenPaw 从一个静态助手转变为持续学习的智能系统。它使 Agent 能够通过 MCP 协议自主创建、审核和安装新技能。

---

## ✨ 功能特性

### 🧬 自我进化
- 自动根据用户需求创建新的 QwenPaw 技能
- 通过 MCP 驱动的反馈循环持续优化技能
- 支持技能从"草稿"到"活跃"状态的审批流程

### 🛡️ AST 安全护盾
- 使用静态代码分析技术（AST）对 AI 生成的代码进行安全审计
- 自动拦截危险操作（如 `rm -rf /`、`format c:` 等）
- 防止恶意代码破坏你的工作区

### 🧠 上下文记忆
- 利用向量嵌入技术维护长期记忆
- 自动进行历史记录审核和知识库更新
- 减少 AI 幻觉，保持回答的一致性

### 🌐 Web 控制台
- 内置可视化仪表板（http://127.0.0.1:8080）
- 实时监控技能进化过程
- 查看活跃技能、进化历史和系统状态

### 🛠️ 零配置安装
- 智能引导系统自动修复环境和配置漂移
- 自动复制技能到工作区
- 自动注入 MCP 客户端配置

### 🧩 模块化设计
- 解耦的核心模块，便于扩展
- **Brain（大脑）**：进化逻辑
- **Lab（实验室）**：技能管理
- **Soul（灵魂）**：人格化记忆
- **Synergy（协同）**：跨 Agent 知识共享
- **Shield（盾牌）**：安全审计

---

## 📋 系统要求

| 项目 | 最低版本 |
|------|---------|
| **QwenPaw** | v1.1.0+ |
| **Python** | 3.10+ |
| **操作系统** | Windows / macOS / Linux |

### Python 依赖

```
fastmcp>=0.1.0
fastapi>=0.100.0
uvicorn>=0.23.0
jinja2>=3.1.0
```

> ⚠️ **注意**：`fastmcp` 需要 Python 3.10+。如果使用 Python 3.9，请使用 QwenPaw 捆绑的 Python 或升级系统 Python。

---

## 🚀 安装指南

### 方式一：使用 QwenPaw CLI（推荐）

```bash
# 1. 克隆仓库或下载压缩包并解压
git clone https://github.com/plhys/qwenpaw-evolution.git
cd qwenpaw-evolution

# 2. 安装插件（确保 QwenPaw 已停止）
qwenpaw plugin install . --force

# 3. 安装依赖
pip install "fastmcp>=0.1.0" "fastapi>=0.100.0" "uvicorn>=0.23.0" "jinja2>=3.1.0"

# 4. 启动 QwenPaw
qwenpaw app
```

### 方式二：手动安装

```bash
# 1. 将插件文件夹复制到 QwenPaw 插件目录
cp -r qwenpaw-evolution ~/.qwenpaw/plugins/qwenpaw-evolution

# 2. 安装依赖
pip install "fastmcp>=0.1.0" "fastapi>=0.100.0" "uvicorn>=0.23.0" "jinja2>=3.1.0"

# 3. 启动 QwenPaw
qwenpaw app
```

### 首次启动

插件首次启动时会自动执行以下操作：
1. ✅ 复制捆绑技能到 `~/.qwenpaw/workspaces/default/skills/`
2. ✅ 在 `skill.json` 中启用技能
3. ✅ 注入 MCP 客户端配置到 `agent.json`
4. ✅ 创建 `.dream_engine_initialized` 标记文件
5. ✅ 启动 Web 控制台（http://127.0.0.1:8080）

---

## 📖 使用方法

### 基本指令

直接对你的 Agent 下达以下指令：

| 指令 | 功能 |
|------|------|
| "整理数据" | 触发梦境循环，自动整理记忆和更新 Wiki |
| "创建一个 XX 技能" | 自动生成新技能并以草稿模式保存 |
| "列出所有技能" | 查看所有管理的技能 |
| "审批 XX 技能" | 将技能从"草稿"升级为"活跃"状态 |
| "查看进化时间线" | 查看 Agent 的成长历史 |

### MCP 工具

插件提供以下 MCP 工具（可通过 Agent 调用）：

| 工具名称 | 功能描述 |
|---------|---------|
| `evolve_create_skill` | 创建新的 QwenPaw 技能 |
| `evolve_run_dream_cycle` | 触发后端梦境循环逻辑 |
| `evolve_approve_skill` | 批准技能从草稿升级为活跃 |
| `evolve_list_skills` | 列出所有被管理的技能 |
| `evolve_get_timeline` | 获取进化时间线和灵魂快照 |
| `evolve_archive_skill` | 移除或归档指定技能 |

### Web 控制台

访问 http://127.0.0.1:8080 可查看：
- 🟢 活跃技能列表
- 📜 进化历史记录
- 📊 系统状态（活跃技能数、隔离区数量）

---

## 🔧 卸载指南

> ⚠️ **卸载操作必须在 QwenPaw 离线状态下进行**

### 步骤 1：停止 QwenPaw

```bash
# 停止正在运行的 QwenPaw 进程
```

### 步骤 2：卸载插件

```bash
qwenpaw plugin uninstall qwenpaw-evolution
```

### 步骤 3：运行清理脚本

```bash
python /path/to/qwenpaw-evolution/uninstall.py
```

清理脚本会删除以下残留配置：
- `agent.json` 中的 `mcp.clients.evolution_engine`
- `skill.json` 中的 `dream_system`
- 标记文件 `.dream_engine_initialized`

### 步骤 4：手动清理（可选）

```bash
# 删除进化技能和数据
rm -rf ~/.qwenpaw/workspaces/default/skills/evolved_skills/
rm -rf ~/.qwenpaw/.dream_engine_plugin_data/
```

---

## 🏗️ 架构说明

### 双通道设计

**热通道（实时）**
```
用户请求 → 技能创建 → 安全审计 → 安装运行
```

**冷通道（梦境循环）**
```
历史审核 → 知识缺口分析 → Wiki 更新
```

### 核心模块

| 模块 | 功能 |
|------|------|
| `engine/brain.py` | 进化大脑 - 技能进化逻辑 |
| `engine/lab.py` | 技能实验室 - 技能状态管理 |
| `engine/soul.py` | 灵魂引擎 - 人格化记忆 |
| `engine/synergy.py` | 协同引擎 - 跨 Agent 知识共享 |
| `engine/shield.py` | 安全盾牌 - AST 代码审计 |
| `engine/cognition.py` | 认知引擎 - 上下文感知 |
| `engine/messenger.py` | 消息系统 - 日志和通知 |
| `lib/skill_manager.py` | 技能管理器 - 核心 CRUD |
| `lib/bootstrap.py` | 引导管理器 - 环境初始化 |
| `lib/console_server.py` | Web 控制台服务 |

---

## 📋 故障排查

### 插件加载但无反应

1. 检查日志中的 `[qwenpaw.plugin.dream_engine]` 条目：
   ```bash
   tail -f ~/.qwenpaw/qwenpaw.log | findstr "dream_engine"
   ```
2. 如果没有日志：删除 `.dream_engine_initialized` 标记文件并重启

### 使用 dream_system 技能时卡住

1. 确认 `fastmcp` 已安装：`pip show fastmcp`
2. 检查 MCP 服务能否启动：`python mcp_server.py`
3. 验证 `agent.json` 中是否有 `mcp.clients.evolution_engine` 配置

### Web 控制台无法访问

1. 端口 8080 可能被占用，修改 `lib/console_server.py` 中的端口
2. 确认 `uvicorn` 和 `fastapi` 已安装：`pip show uvicorn fastapi`

### Python 3.9 安装失败

`fastmcp>=0.1.0` 需要 Python 3.10+。解决方案：
- 使用 QwenPaw 捆绑的 Python
- 或升级系统 Python：`brew install python@3.12`

---

## 📄 开源协议

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

*最后更新：2026-04-13*