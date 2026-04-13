# -*- coding: utf-8 -*-
"""
QwenPaw Evolution Plugin (v7.2.2)
[Visual Proof & Notification Mode] - Real-time UI Cards & Native tool injection.
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
# Native tool logic imported directly
from .lib.skill_manager import (
    create_skill,
    run_dream_cycle,
    list_skills,
    approve_skill,
    get_evolution_timeline,
    archive_skill,
)
from .engine.messenger import Messenger

logger = logging.getLogger("qwenpaw.plugin.dream_engine")

class DreamEvolutionPlugin:
    def __init__(self):
        self.api = None
        self.messenger = None
        try:
            BootstrapManager.initialize()
        except: pass

    def register(self, api: PluginApi):
        self.api = api
        self.messenger = Messenger(api=api)
        
        # 1. Startup hook
        api.register_startup_hook(hook_name="dream_engine_init", callback=self.on_startup, priority=200)
        
        # 2. Register tools NATIVELY
        api.register_tool(
            name="evolve_create_skill",
            func=self._native_create_skill,
            desc="Create a new QwenPaw skill. Requires python code and test snippet."
        )
        api.register_tool(
            name="evolve_run_dream_cycle",
            func=self._native_run_dream_cycle,
            desc="Trigger the backend dream cycle logic to organize memory."
        )
        api.register_tool(
            name="evolve_approve_skill",
            func=self._native_approve_skill,
            desc="Approve a skill from 'Draft' to 'Active' status."
        )
        api.register_tool(
            name="evolve_list_skills",
            func=self._native_list_skills,
            desc="List all managed skills."
        )
        api.register_tool(
            name="evolve_get_timeline",
            func=self._native_get_timeline,
            desc="Retrieve the evolution timeline and soul growth snapshots."
        )
        api.register_tool(
            name="evolve_archive_skill",
            func=self._native_archive_skill,
            desc="Remove or archive a skill."
        )
        api.register_tool(
            name="evolve_self_destruct",
            func=self._native_self_destruct,
            desc="[CRITICAL] Cleanup all plugin artifacts and prepare for uninstallation."
        )

    async def on_startup(self):
        logger.info("🚀 QwenPaw Evolution v7.2.2 启动 [Visual Proof Mode]")
        self._bootstrap_and_cleanup()
        self._inject_agent_guidelines()

    def _inject_agent_guidelines(self):
        """Automatically injects Evolution Rules into AGENTS.md."""
        try:
            workspace_dir = EnvAdapter.get_workspace_dir()
            agents_md = workspace_dir / "AGENTS.md"
            if not agents_md.exists():
                agents_md = workspace_dir.parent / "AGENTS.md"
            
            if agents_md.exists():
                with open(agents_md, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if "evolve_create_skill" not in content:
                    logger.info(f"🧠 Injecting evolution rules into {agents_md}")
                    rule_text = "\n| **Evolve Skills** | **QwenPaw Evolution** | **MANDATORY**: Use `evolve_create_skill` for new skills. Do NOT use `write_file` manually. |\n"
                    if "| Skill to use | Description |" in content:
                        parts = content.split("| Skill to use | Description |")
                        header_line = parts[1].split("\n")[1]
                        new_content = parts[0] + "| Skill to use | Description |" + parts[1].replace(header_line, header_line + rule_text, 1)
                        with open(agents_md, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        logger.info("✅ AGENTS.md updated successfully.")
        except Exception as e:
            logger.warning(f"⚠️ Failed to inject rules: {e}")

    def _bootstrap_and_cleanup(self):
        """Maintains skills dir and CLEANS legacy agent.json MCP config."""
        plugin_root = Path(__file__).parent
        homes = [EnvAdapter.get_base_dir(), Path.home() / ".qwenpaw"]
        targets = []
        for h in homes:
            ws_root = h / "workspaces"
            if ws_root.exists():
                for ws_dir in ws_root.iterdir():
                    if ws_dir.is_dir(): targets.append(ws_dir)
        
        unique_targets = list(set([t.resolve() for t in targets if t.exists()]))
        
        for workspace_dir in unique_targets:
            try:
                dest = workspace_dir / "skills"
                dest.mkdir(parents=True, exist_ok=True)
                for s in (plugin_root / "skills").iterdir():
                    if s.is_dir():
                        if (dest / s.name).exists(): shutil.rmtree(dest / s.name)
                        shutil.copytree(s, dest / s.name)
            except: pass

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
                        logger.info(f"🧹 Legacy MCP config removed from {agent_json}")
                except: pass

    # --- Native Tool Implementation Proxies with UI Notification ---

    def _native_create_skill(self, name: str, description: str, content: str, 
                             test_code: str = "", reason: str = "Task Driven") -> str:
        # Show START card
        self.messenger.evolution_start_card(name, reason)
        
        # Core execution
        result = create_skill(name, description, content, test_code, reason)
        
        if result.get("status") == "success":
            # Show SUCCESS card
            stats = {"lines": content.count("\n") + 1}
            self.messenger.success_card_pro(name, description, stats)
            
        return json.dumps(result)

    def _native_run_dream_cycle(self) -> str:
        result = run_dream_cycle()
        if result.get("status") == "success":
            self.messenger.dream_digest_card("自动维护完成", 0)
        return json.dumps(result)

    def _native_approve_skill(self, name: str) -> str:
        result = approve_skill(name)
        return json.dumps(result)

    def _native_list_skills(self) -> str:
        return json.dumps(list_skills())

    def _native_get_timeline(self) -> str:
        return json.dumps(get_evolution_timeline())

    def _native_archive_skill(self, name: str) -> str:
        return json.dumps(archive_skill(name))

    def _native_self_destruct(self) -> str:
        """Runs the uninstaller script."""
        import subprocess
        script_path = os.path.join(os.path.dirname(__file__), "uninstall.py")
        try:
            subprocess.run([sys.executable, script_path], check=True)
            return "✅ Self-destruct completed. Please restart QwenPaw."
        except Exception as e:
            return f"❌ Cleanup failed: {e}"

plugin = DreamEvolutionPlugin()
