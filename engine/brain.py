import threading
import time
import logging
import json
import os
import uuid
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from .shield import SecurityShield
from .messenger import Messenger
from .cognition import CognitionEngine
from .synergy import SynergyEngine
from .soul import SoulEngine

try:
    from ..lib.env_adapter import EnvAdapter
    from ..lib.dep_manager import DependencyManager
except (ImportError, ValueError):
    from lib.env_adapter import EnvAdapter
    from lib.dep_manager import DependencyManager

logger = logging.getLogger("qwenpaw.plugin.dream_engine.brain")

class EvolutionBrain:
    """The Sentient Evolution logic (v7.1.0). Supports Unit Tests & Backend-driven Dreams."""
    
    def __init__(self, agent_id="default"):
        self.agent_id = agent_id
        self.messenger = Messenger(agent_id)
        self.shield = SecurityShield()
        self.dep_manager = DependencyManager()
        self.cognition = CognitionEngine(agent_id)
        self.synergy = SynergyEngine()
        self.soul = SoulEngine(agent_id)
        self.skills_dir = EnvAdapter.get_evolved_skills_dir(agent_id)
        self.history_file = EnvAdapter.get_plugin_data_dir() / f"history_{agent_id}.json"
        self._init_history()

    def _init_history(self):
        if not self.history_file.exists():
            with open(self.history_file, "w") as f:
                json.dump([], f)

    def evolve_skill(self, name: str, description: str, python_code: str, 
                     test_code: str = "", reason: str = "任务驱动", 
                     is_draft: bool = True):
        """
        Evolution with Unit Tests and Self-Healing error feedback.
        """
        self.messenger.evolution_start_card(reason)
        
        # 1. Security Audit
        self.messenger.thinking(f"安全审计: `{name}`", progress=10)
        is_safe, audit_msg = self.shield.audit_code(python_code)
        if not is_safe:
            return False, f"SECURITY_BLOCK: {audit_msg}"
            
        # 2. Dependency Resolution
        self.messenger.thinking(f"解析依赖: `{name}`", progress=30)
        self.dep_manager.resolve_dependencies(python_code)
            
        # 3. Unit Test & Validation (Self-Healing feedback)
        self.messenger.thinking(f"运行单元测试: `{name}`", progress=60)
        test_success, test_msg = self._run_validation(name, python_code, test_code)
        if not test_success:
            self.messenger.warning(f"测试失败", detail=test_msg)
            return False, f"TEST_FAILED: {test_msg}\n请根据 Traceback 修复代码逻辑后再尝试。"
            
        # 4. Persistence
        status = "draft" if is_draft else "active"
        skill_path = self.skills_dir / f"{name}.py"
        try:
            with open(skill_path, "w", encoding="utf-8") as f:
                f.write(python_code)
            
            # 5. Evolution Timeline & Soul Snapshot
            soul_vector = self.soul.get_current_identity_vector()
            self._log_event("evolution", name, {
                "status": status,
                "reason": reason,
                "soul_snapshot": soul_vector,
                "lines": len(python_code.splitlines())
            })
            
            # 6. Cognition Manifest Update
            self.cognition.register_new_skill(name, description, status=status)
            
            # Success Notification
            status_tag = " [⏳ 待审核草稿]" if is_draft else " [✅ 已激活]"
            self.messenger.success_card_pro(name + status_tag, description, python_code, {"size_kb": len(python_code)/1024, "lines": len(python_code.splitlines())})
            
            return True, "Success"
        except Exception as e:
            logger.error(f"Save failed: {e}")
            return False, str(e)

    def run_dream_logic(self):
        """
        v7.1.0: Backend-driven Dream Cycle. 
        Moves heavy processing from LLM to Python to prevent hanging.
        """
        self.messenger.info("🌙 启动后台梦境整理任务...")
        
        # Determine working directory from EnvAdapter
        working_dir = EnvAdapter.get_workspace_dir()
        memory_dir = working_dir / "memory"
        wiki_dir = memory_dir / "wiki"
        archive_raw = memory_dir / "archive" / "raw"
        
        # 1. Ensure dirs
        for d in [wiki_dir, archive_raw, wiki_dir / "Projects", wiki_dir / "Entities"]:
            d.mkdir(parents=True, exist_ok=True)

        # 2. Scan compact files
        compact_files = list(memory_dir.glob("compact_*.md"))[:5]
        if not compact_files:
            self.messenger.info("🌙 暂无待处理记忆。")
            return True, "No memory fragments found."

        processed_count = 0
        for cf in compact_files:
            try:
                # In v7.1.0 we move to archive to unblock the system.
                # Fact extraction logic can be added here later.
                dest = archive_raw / cf.name
                if dest.exists():
                    dest.unlink()
                cf.replace(dest)
                processed_count += 1
                logger.info(f"Processed memory fragment: {cf.name}")
            except Exception as e:
                logger.error(f"Failed to process {cf.name}: {e}")

        # 3. Update Wiki Index
        readme = wiki_dir / "README.md"
        if not readme.exists():
            with open(readme, "w", encoding="utf-8") as f:
                f.write("# 📚 Knowledge Wiki\n\n## Auto-maintained by v7.1.0")

        self.messenger.info(f"✅ 梦境整理完成：清理了 {processed_count} 个碎片。")
        return True, f"SUCCESS: Processed {processed_count} files."

    def _run_validation(self, name, code, test_code):
        """Runs the code and optional test_code in a isolated subprocess."""
        temp_file = self.skills_dir / f"_temp_test_{uuid.uuid4().hex[:8]}.py"
        full_content = code + "\n\n# --- UNIT TEST ---\n" + test_code
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(full_content)
            
            result = subprocess.run(
                [sys.executable, str(temp_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "All tests passed."
            else:
                return False, result.stderr or result.stdout
        except subprocess.TimeoutExpired:
            return False, "Validation Timeout: Execution took longer than 30s."
        except Exception as e:
            return False, str(e)
        finally:
            if temp_file.exists():
                temp_file.unlink()

    def _log_event(self, event_type, name, detail):
        try:
            with open(self.history_file, "r+") as f:
                data = json.load(f)
                data.append({
                    "id": str(uuid.uuid4())[:8], 
                    "type": event_type, 
                    "name": name, 
                    "detail": detail, 
                    "timestamp": datetime.now().isoformat()
                })
                f.seek(0); json.dump(data, f, indent=2); f.truncate()
        except: pass
