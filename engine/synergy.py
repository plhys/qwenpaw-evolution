import json
import logging
from pathlib import Path
try:
    from ..lib.env_adapter import EnvAdapter
except (ImportError, ValueError):
    from lib.env_adapter import EnvAdapter

logger = logging.getLogger("qwenpaw.DreamEngine.Synergy")

class SynergyEngine:
    """The Hive-Mind Sync layer for cross-agent skill sharing and QA infusion (v6.5.0)."""
    
    def __init__(self, agent_id="default"):
        self.agent_id = agent_id
        self.data_dir = EnvAdapter.get_plugin_data_dir()
        self.shared_skills_dir = self.data_dir / "shared_evolution"
        self.qa_memory_file = self.data_dir / "qa_infusion_queue.json"
        
        # Ensure directories
        self.shared_skills_dir.mkdir(parents=True, exist_ok=True)
        self._init_qa_queue()

    def _init_qa_queue(self):
        if not self.qa_memory_file.exists():
            with open(self.qa_memory_file, "w") as f:
                json.dump([], f)

    def share_skill_globally(self, name: str, code: str, description: str):
        """Make a skill available to all Agents in the QwenPaw environment."""
        shared_path = self.shared_skills_dir / f"{name}.py"
        with open(shared_path, "w", encoding="utf-8") as f:
            f.write(f'# Shared Skill: {name}\n# Description: {description}\n\n{code}')
        logger.info(f"Skill '{name}' promoted to Global Shared Hub.")

    def queue_qa_knowledge(self, question: str, answer: str):
        """Queue a knowledge nugget for infusion into QwenPaw's QA Agent."""
        try:
            with open(self.qa_memory_file, "r+") as f:
                data = json.load(f)
                data.append({
                    "id": len(data) + 1,
                    "q": question,
                    "a": answer,
                    "status": "pending"
                })
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            logger.info(f"Knowledge queued for QA infusion: {question[:30]}...")
        except Exception as e:
            logger.error(f"QA queueing failed: {e}")

    def get_all_shared_skills(self):
        """Retrieve all skills from the shared hub."""
        return [f.stem for f in self.shared_skills_dir.glob("*.py")]
