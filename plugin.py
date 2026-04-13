# -*- coding: utf-8 -*-
"""
QwenPaw Evolution Plugin (v7.3.2)
[Physical Sync Mode] - Bypasses unstable PluginApi by syncing skills directly.
"""

import json
import logging
import os
import shutil
import sys
from pathlib import Path

from qwenpaw.plugins.api import PluginApi
from .lib.env_adapter import EnvAdapter
from .lib.bootstrap import BootstrapManager

logger = logging.getLogger("qwenpaw.plugin.dream_engine")

class DreamEvolutionPlugin:
    def __init__(self):
        try:
            BootstrapManager.initialize()
        except: pass

    def register(self, api: PluginApi):
        # We still register the startup hook to handle the physical file syncing
        api.register_startup_hook(hook_name="dream_engine_init", callback=self.on_startup, priority=200)
        
        # We TRY to register tools, but if it fails (due to old API), 
        # the Agent will still find the "dream_system" skill in its workspace.
        try:
            api.register_tool(
                name="evolve_create_skill",
                func=self._native_noop,
                desc="[DEPRECATED] Use the dream_system skill in your workspace instead."
            )
        except:
            logger.info("PluginApi.register_tool not supported, skipping code injection.")

    async def on_startup(self):
        logger.info("🚀 QwenPaw Evolution v7.3.2 启动 [Physical Sync Mode]")
        self._bootstrap_all_workspaces()

    def _bootstrap_all_workspaces(self):
        """Forces the 'dream_system' and 'dream_engine' skills into ALL workspace skills folders."""
        plugin_root = Path(__file__).parent
        
        # 1. Gather all possible workspaces
        homes = [EnvAdapter.get_base_dir(), Path.home() / ".qwenpaw"]
        # Also check common Windows paths if not found
        if sys.platform == "win32":
            homes.append(Path(os.environ["USERPROFILE"]) / ".qwenpaw")
            
        targets = []
        for h in homes:
            ws_root = h / "workspaces"
            if ws_root.exists():
                for ws_dir in ws_root.iterdir():
                    if ws_dir.is_dir(): targets.append(ws_dir)
        
        unique_targets = list(set([t.resolve() for t in targets if t.exists()]))
        
        # 2. Force Sync
        for workspace_dir in unique_targets:
            logger.info(f"📁 Syncing evolution engine to workspace: {workspace_dir.name}")
            dest = workspace_dir / "skills"
            dest.mkdir(parents=True, exist_ok=True)
            
            # Sync the core evolution skills
            source_skills = plugin_root / "skills"
            if source_skills.exists():
                for s_dir in source_skills.iterdir():
                    if s_dir.is_dir():
                        target_path = dest / s_dir.name
                        # Safety: always overwrite to ensure latest version
                        if target_path.exists(): shutil.rmtree(target_path)
                        shutil.copytree(s_dir, target_path)
                        logger.info(f"   ✅ Injected skill: {s_dir.name}")

            # 3. Clean up legacy MCP entries from agent.json to stop the WinError 267
            self._cleanup_agent_json(workspace_dir)

    def _cleanup_agent_json(self, workspace_dir):
        agent_json = workspace_dir / "agent.json"
        if agent_json.exists():
            try:
                with open(agent_json, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                modified = False
                for m_key in ["mcp", "mcp_servers"]:
                    if m_key in data:
                        for sub in ["clients", "servers"]:
                            if sub in data[m_key] and "evolution_engine" in data[m_key][sub]:
                                del data[m_key][sub]["evolution_engine"]
                                modified = True
                if modified:
                    with open(agent_json, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    logger.info(f"   🧹 Legacy MCP config scrubbed.")
            except: pass

    def _native_noop(self, *args, **kwargs):
        return "Please use the dream_system skill directly."

plugin = DreamEvolutionPlugin()
