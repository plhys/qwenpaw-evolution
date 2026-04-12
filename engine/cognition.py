import json
import logging
from pathlib import Path
try:
    from ..lib.env_adapter import EnvAdapter
except (ImportError, ValueError):
    from lib.env_adapter import EnvAdapter

logger = logging.getLogger("qwenpaw.plugin.dream_engine.cognition")

class CognitionEngine:
    """The Intelligence Perception layer with Intent-Matching (v7.0.0)."""
    
    def __init__(self, agent_id="default"):
        self.agent_id = agent_id
        self.data_dir = EnvAdapter.get_plugin_data_dir()
        self.manifest_file = self.data_dir / "skills_manifest.json"
        self._init_manifest()

    def _init_manifest(self):
        if not self.manifest_file.exists():
            with open(self.manifest_file, "w") as f:
                json.dump({}, f)

    def register_new_skill(self, name: str, description: str, status: str = "active"):
        """Update the manifest with status awareness."""
        try:
            with open(self.manifest_file, "r+") as f:
                data = json.load(f)
                data[name] = {
                    "description": description,
                    "status": status,
                    "importance": 50
                }
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
        except Exception as e:
            logger.error(f"Manifest update failed: {e}")

    def get_awareness_prompt(self, user_query: str = "", soul_context: str = "") -> str:
        """
        v7.0.0: Dynamic Loader using keyword-based intent matching.
        Reduces Token usage by only loading relevant skills.
        """
        try:
            with open(self.manifest_file, "r") as f:
                data = json.load(f)
            
            # 1. Filter active skills
            active_skills = {k: v for k, v in data.items() if v.get("status") == "active"}
            if not active_skills and not soul_context:
                return ""

            # 2. Match Intent (Keyword-based for performance)
            matched = {}
            if not user_query:
                # Default: Load high importance skills
                matched = {k: v for k, v in active_skills.items() if v.get("importance", 0) >= 80}
            else:
                q = user_query.lower()
                for name, info in active_skills.items():
                    desc = info.get("description", "").lower()
                    if name.lower() in q or any(word in q for word in desc.split()):
                        matched[name] = info
            
            if not matched and not soul_context:
                return ""

            # 3. Format Prompt
            prompt_parts = [f"- {name}: {info['description']}" for name, info in matched.items()]
            skills_section = ""
            if prompt_parts:
                skills_section = (
                    "\n[CAPABILITIES: DYNAMICALLY LOADED]\n"
                    "You have evolved following skills. Use them proactively:\n" + "\n".join(prompt_parts) + "\n"
                )
            
            return skills_section + soul_context
        except Exception as e:
            logger.error(f"Awareness generation failed: {e}")
            return soul_context
