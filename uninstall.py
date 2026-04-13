#!/usr/bin/env python3
"""
QwenPaw Evolution - Robust Uninstall Script (v7.1.9)
Usage: python uninstall.py

This script performs a deep cleanup of all artifacts left by the plugin:
1. Kills running evolution_engine MCP processes.
2. Cleans agent.json in ALL workspaces (removes mcp configuration).
3. Cleans skill.json in ALL workspaces (removes skill registration).
4. Removes skill folders and data files from ALL workspaces.
5. Removes legacy plugin data directories.
"""

import json
import os
import signal
import subprocess
import shutil
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("uninstall")

def get_base_dirs():
    """Get potential QwenPaw base directories."""
    homes = []
    qwen_home = os.environ.get("QWENPAW_HOME")
    if qwen_home:
        homes.append(Path(qwen_home))
    
    # Common default location
    qwen_path = Path.home() / ".qwenpaw"
    homes.append(qwen_path)
    
    # Current dir if it looks like a base dir
    if (Path.cwd() / "workspaces").exists():
        homes.append(Path.cwd())
        
    return list(set([h.resolve() for h in homes if h.exists()]))

def get_all_workspaces():
    """Discover all workspaces across all base directories."""
    workspaces = []
    for base in get_base_dirs():
        ws_root = base / "workspaces"
        if ws_root.exists():
            for ws_dir in ws_root.iterdir():
                if ws_dir.is_dir():
                    workspaces.append(ws_dir.resolve())
    return list(set(workspaces))

def clean_json_file(file_path, remove_keys, remove_from_mcp=True):
    """Safely remove keys from a JSON file, including deep MCP structures."""
    if not file_path.exists():
        return False

    try:
        # Use utf-8-sig to handle potential BOM from Windows
        with open(file_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            
        modified = False
        
        # 1. Direct key removal (for skill.json)
        for key in remove_keys:
            if key in data:
                del data[key]
                modified = True
        
        # 2. MCP structure removal (for agent.json)
        if remove_from_mcp:
            for mcp_key in ["mcp", "mcp_servers"]:
                if mcp_key in data:
                    for sub_key in ["clients", "servers"]:
                        if sub_key in data[mcp_key]:
                            for target in ["evolution_engine", "dream_engine"]:
                                if target in data[mcp_key][sub_key]:
                                    del data[mcp_key][sub_key][target]
                                    modified = True
                                    
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
    except Exception as e:
        logger.error(f"Failed to process {file_path.name}: {e}")
    return False

def run_cleanup():
    logger.info("🧹 Starting QwenPaw Evolution Deep Uninstallation...")

    # 1. Kill running processes
    logger.info("🔍 1. Killing evolution_engine processes...")
    try:
        # Search for mcp_server.py or processes related to this plugin
        cmd = "pgrep -f mcp_server.py"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split("\n")
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGTERM)
                    logger.info(f"   ✅ Terminated PID {pid}")
                except: pass
        else:
            logger.info("   ℹ️ No active processes found.")
    except Exception as e:
        logger.warning(f"   ⚠️ Process cleanup error: {e}")

    # 2. Discover and clean workspaces
    workspaces = get_all_workspaces()
    logger.info(f"🔍 2. Found {len(workspaces)} workspaces to clean.")
    
    plugin_skills = ["dream_system", "qwenpaw_log_diagnose", "evolved_skills"]
    
    for ws in workspaces:
        logger.info(f"   📂 Cleaning workspace: {ws.name}")
        
        # Clean agent.json
        agent_json = ws / "agent.json"
        if clean_json_file(agent_json, [], remove_from_mcp=True):
            logger.info(f"      ✅ Cleaned agent.json")
            
        # Clean skill.json
        skill_json = ws / "skill.json"
        if clean_json_file(skill_json, plugin_skills, remove_from_mcp=False):
            logger.info(f"      ✅ Cleaned skill.json")
            
        # Remove skill folders
        skills_dir = ws / "skills"
        if skills_dir.exists():
            for s_name in plugin_skills:
                target = skills_dir / s_name
                if target.exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                    logger.info(f"      ✅ Removed skill artifact: {s_name}")
                    
        # Remove markers
        marker = ws / ".dream_engine_initialized"
        if marker.exists():
            marker.unlink()
            logger.info(f"      ✅ Removed initialization marker")

    # 3. Clean global/plugin data
    logger.info("🗑️ 3. Cleaning global data directories...")
    base_dirs = get_base_dirs()
    for base in base_dirs:
        data_paths = [
            base / ".dream_engine_plugin_data",
            base / "plugins" / "dream-evolution-engine",
            base / "plugins" / "qwenpaw-evolution" / "data"
        ]
        for path in data_paths:
            if path.exists():
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                    logger.info(f"   ✅ Removed data path: {path}")
                except Exception as e:
                    logger.error(f"   ❌ Error removing {path}: {e}")

    logger.info("\n✨ Cleanup finished successfully.")
    logger.info("👉 You can now safely remove the plugin folder if you haven't already.")
    logger.info("👉 Restart QwenPaw to apply all changes.")

if __name__ == "__main__":
    run_cleanup()
