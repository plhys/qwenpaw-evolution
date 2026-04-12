# QwenPaw Evolution

> **A Self-Evolution Engine for QwenPaw** — v7.1.8

**QwenPaw Evolution** transforms QwenPaw from a static assistant into a continuously learning system. It enables the agent to create, audit, and install new skills autonomously via the MCP protocol.

## ✨ Key Features

- **🧬 Self-Evolving**: Automatically creates and installs new skills through an MCP-driven feedback loop.
- **🛡️ AST Security Shield**: Every generated code snippet is statically analyzed to prevent destructive operations (e.g., `rm -rf /`).
- **🧠 Contextual Memory**: Utilizes vector embeddings to maintain long-term memory and avoid hallucination.
- **🛠️ Zero-Config Installation**: Smart bootstrap system that automatically repairs environment and configuration drifts.
- **🧩 Modular Design**: Decoupled core modules (Brain, Lab, Synergy, Soul) for easy extension.
- **🌐 Web Console**: Visual dashboard at `:8080` to monitor the evolution process.

---

## 🚀 Installation

### Prerequisites

- **QwenPaw v1.1.0+** installed and running
- **Python 3.10+** (required by `fastmcp` dependency)

### Step 1: Install Plugin

```bash
qwenpaw plugin install /path/to/qwenpaw-dream-engine
```

> ⚠️ **QwenPaw does NOT auto-install plugin dependencies.** You must install them manually.

### Step 2: Install Dependencies

```bash
pip install "fastmcp>=0.1.0" "fastapi>=0.100.0" "uvicorn>=0.23.0" "jinja2>=3.1.0"
```

> Python 3.9 users: `fastmcp` requires Python 3.10+. Use QwenPaw's bundled Python or upgrade your system Python.

### Step 3: Start QwenPaw

```bash
qwenpaw app
```

On first run, the engine will:
1. Copy bundled skills to `~/.qwenpaw/workspaces/default/skills/`
2. Enable them in `skill.json`
3. Inject MCP client config into `agent.json` (`mcp.clients.evolution_engine`)
4. Create `.dream_engine_initialized` marker
5. Start the Web Console on `http://127.0.0.1:8080`

### Step 4: Verify

1. Open the Web Console: `http://127.0.0.1:8080`
2. Check QwenPaw logs for DreamEngine entries:
   ```bash
   tail -f ~/.qwenpaw/qwenpaw.log | grep DreamEngine
   ```
3. Ask your agent: "使用 dream_system 技能"

---

## 🗑️ Uninstallation

> ⚠️ **Plugin operations must be performed while QwenPaw is OFFLINE.**

### Step 1: Stop QwenPaw

```bash
# Stop the running QwenPaw process
```

### Step 2: Remove Plugin

```bash
qwenpaw plugin uninstall qwenpaw-dream-engine
```

This removes the plugin from `~/.qwenpaw/plugins/`.

### Step 3: Clean Residual Configuration

```bash
python /path/to/qwenpaw-dream-engine/uninstall.py
```

The uninstall script cleans up what `qwenpaw plugin uninstall` does NOT remove:

| Item | Why it's not auto-cleaned |
|------|--------------------------|
| `agent.json` → `mcp.clients.evolution_engine` | QwenPaw only removes the plugin dir, not config edits |
| `skill.json` → `dream_system` | Skills are workspace-level, not plugin-level |
| `~/.qwenpaw/workspaces/default/.dream_engine_initialized` | Marker file for bootstrap |

### Step 4: Manual Cleanup (Optional)

Remove evolved skills and data:

```bash
rm -rf ~/.qwenpaw/workspaces/default/skills/evolved_skills/
rm -rf ~/.qwenpaw/workspaces/default/skill_scanner_blocked.json
rm -rf ~/.qwenpaw/.dream_engine_plugin_data/
```

---

## 🏗️ Architecture

The engine operates on two paths:

1. **Hot Path (Real-time)**
   `Agent Request` → `Skill Creation` → `Security Audit` → `Install & Run`

2. **Cold Path (Dream Cycle)**
   `History Review` → `Knowledge Gap Analysis` → `Wiki Update`

---

## 📋 Troubleshooting

### Plugin loads but nothing happens

1. Check `qwenpaw.log` for `[qwenpaw.DreamEngine]` entries:
   ```bash
   tail -f ~/.qwenpaw/qwenpaw.log | grep DreamEngine
   ```
2. If no entries: the `on_startup` hook may not have fired. Delete `.dream_engine_initialized` marker and restart.

### Agent hangs when using dream_system skill

1. Ensure `fastmcp` is installed: `pip show fastmcp`
2. Check if MCP server can start: `python3 /path/to/mcp_server.py`
3. Verify `agent.json` has `mcp.clients.evolution_engine` config

### Web Console not accessible

1. Port 8080 may be in use. Change `ConsoleServer(port=8081)` in `plugin.py`
2. Check for `uvicorn` and `fastapi`: `pip show uvicorn fastapi`

### Dependency install fails on Python 3.9

`fastmcp>=0.1.0` requires Python 3.10+. Solutions:
- Use QwenPaw's bundled Python (script install uses `uv` with correct version)
- Upgrade system Python: `brew install python@3.12`

---

## 📄 License

MIT License
