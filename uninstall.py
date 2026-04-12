#!/usr/bin/env python3
"""
QwenPaw Dream Engine - Uninstall Script
Usage: python uninstall.py
This script performs a thorough cleanup:
1. Kills running processes.
2. Cleans agent.json.
3. Removes installed skills from workspace.
4. Removes initialization markers.
"""

import json
import os
import signal
import subprocess
from pathlib import Path


def get_base_dir():
    """Get QwenPaw base dir (respects QWENPAW_HOME env var)."""
    qwen_home = os.environ.get("QWENPAW_HOME")
    if qwen_home:
        return Path(qwen_home)

    qwen_path = Path.home() / ".qwenpaw"
    if qwen_path.exists():
        return qwen_path

    return Path.cwd()


def run_cleanup():
    print("🧹 Starting QwenPaw Dream Engine Uninstallation Cleanup...")

    base_dir = get_base_dir()
    workspace_dir = base_dir / "workspaces" / "default"
    agent_json = workspace_dir / "agent.json"

    # 1. Kill running MCP processes
    print("🔍 1. Killing running processes...")
    try:
        result = subprocess.run(
            ["pgrep", "-f", "mcp_server.py"], capture_output=True, text=True
        )
        if result.returncode == 0:
            pids = result.stdout.strip().split("\n")
            for pid in pids:
                print(f"   🚫 Killing PID: {pid}")
                os.kill(int(pid), signal.SIGTERM)
            print("   ✅ Processes killed.")
        else:
            print("   ℹ️ No running processes found.")
    except Exception as e:
        print(f"   ⚠️ Error killing processes: {e}")

    # 2. Clean agent.json (reads same keys plugin.py writes to)
    print("🔧 2. Cleaning agent.json...")
    if agent_json.exists():
        try:
            with open(agent_json, "r", encoding="utf-8") as f:
                data = json.load(f)

            modified = False
            # Check all possible MCP key locations (same keys plugin.py writes to)
            for mcp_key in ["mcp", "mcp_servers"]:
                if mcp_key in data:
                    # Check 'servers' (what plugin.py writes)
                    if (
                        "servers" in data[mcp_key]
                        and "evolution_engine" in data[mcp_key]["servers"]
                    ):
                        del data[mcp_key]["servers"]["evolution_engine"]
                        modified = True
                    # Check 'clients' (legacy/other versions)
                    if (
                        "clients" in data[mcp_key]
                        and "evolution_engine" in data[mcp_key]["clients"]
                    ):
                        del data[mcp_key]["clients"]["evolution_engine"]
                        modified = True

            if modified:
                with open(agent_json, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print("   ✅ Removed MCP config.")
            else:
                print("   ℹ️ No MCP config found.")
        except Exception as e:
            print(f"   ❌ Failed to clean agent.json: {e}")

    # 3. Remove Workspace Artifacts (Skills & Markers) — dynamic discovery
    print("🗑️ 3. Cleaning workspace artifacts...")
    artifacts = []

    # Dynamically find installed skills from this plugin
    plugin_skills_dir = Path(__file__).parent / "skills"
    if plugin_skills_dir.exists() and workspace_dir.exists():
        skills_dest = workspace_dir / "skills"
        if skills_dest.exists():
            for skill in plugin_skills_dir.iterdir():
                if skill.is_dir():
                    artifacts.append(skills_dest / skill.name)

    # Always clean the initialization marker
    artifacts.append(workspace_dir / ".dream_engine_initialized")

    for artifact in artifacts:
        if artifact.exists():
            if artifact.is_dir():
                import shutil

                shutil.rmtree(artifact)
                print(f"   ✅ Removed directory: {artifact.name}")
            else:
                artifact.unlink()
                print(f"   ✅ Removed file: {artifact.name}")

    print("\n✅ Cleanup complete.")
    print("👉 You can now safely delete the plugin folder.")


if __name__ == "__main__":
    run_cleanup()
