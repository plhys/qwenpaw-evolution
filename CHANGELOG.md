# Changelog

All notable changes to this project will be documented in this file.

## [7.1.4] - 2026-04-13
### 🔧 Windows Compatibility
- **Python Path Fix**: Explicitly using `sys.executable` for the MCP command to ensure compatibility with Windows environments where `python3` is not in the PATH.
- **Enhanced Injection Logic**: Double-checking command path before writing to `agent.json`.
### 🔍 Visibility & Verification
- **Verification Loop**: Added immediate file read-back after injecting MCP config to verify data integrity.
- **Enhanced Logging**: Added high-visibility console logs (🔥 [验证成功]) to confirm MCP availability on startup.
- **Diagnostics Skill**: Updated `qwenpaw_log_diagnose` to provide a clear SOP for manual MCP state inspection.
### 🔧 Robust Workspace Discovery
- **Enhanced Path Detection**: Refactored `_bootstrap_workspace` to proactively search for `agent.json` in multiple potential locations (environment variables, parent directories, default paths).
- **Auto-Correction**: Ensured that the parent directory of `agent.json` is created if missing, and the MCP configuration is forcefully injected with verified absolute paths.
- **Improved Error Logging**: Detailed logging for each stage of the bootstrap process to aid in remote diagnosis.
### 🔧 Critical MCP Fix
- **Forced MCP Injection**: Refactored `_bootstrap_workspace` to bypass the `.dream_engine_initialized` marker for MCP configuration. It now ensures `evolution_engine` is always present and correctly path-mapped in `agent.json` on every startup.
- **Path Validation**: Automatically detects and repairs `mcp_server.py` path if the plugin was moved.
### 🚀 Stabilized Dream Cycle
- **Backend-driven logic**: Moved heavy processing (file scanning, archiving) from LLM instructions to Python backend to prevent UI hanging.
- **Forced Skill Sync**: `plugin.py` now forcefully overwrites workspace `SKILL.md` files on startup to ensure protocol consistency.
- **Improved Messenger**: Standardized logging namespace to `qwenpaw.plugin.dream_engine` to prevent stdout corruption in MCP sessions.

## [7.0.0] - 2026-04-12
### ✨ Sentient Update (Major Architecture Upgrade)
- **Self-Healing 2.0**: Implemented automatic error feedback loop. If a newly evolved skill fails, the traceback is sent back to the Agent for self-repair.
- **Unit-Test Guard**: Required LLM to generate unit tests for new skills. Only skills passing local validation are saved.
- **Draft Mode**: Introduced "Human-in-the-loop" safety. New skills are created as `draft` and require `evolve_approve_skill` to activate.
- **Dynamic Intent Matching**: Refactored `CognitionEngine` to load skills dynamically based on user query keywords, significantly reducing Token usage.
- **Evolution Timeline**: Added `soul_snapshot` vectorization to track agent personality drift over time (Data/Dev/Office/Web focus).

## [6.9.0] - 2026-04-12
### 🔧 Install / Uninstall Sync
- **Fixed `on_startup` async bug**: Aligned with QwenPaw v1.1.0+ plugin API.
- **Fixed MCP path discovery**: Now uses `sys.executable` instead of hardcoded `python3` for better venv support.
- **Added `BootstrapManager`**: Graceful handling of bootstrap failures.

## [6.6.0] - 2026-04-12
### 🗑️ Breaking Changes
- **Removed CoPaw Compatibility**: Exclusively targets QwenPaw v1.1.0+.
- **Updated `plugin.json`**: Requirements synced.

## [6.5.0] - 2026-04-12
### ✨ Features
- Added AST Security Shield for static code analysis.
- Added Web Console Sidecar UI.
