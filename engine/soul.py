import json
import logging
from collections import Counter
from pathlib import Path
try:
    from ..lib.env_adapter import EnvAdapter
except (ImportError, ValueError):
    from lib.env_adapter import EnvAdapter

logger = logging.getLogger("qwenpaw.plugin.dream_engine.soul")

class SoulEngine:
    """The Capability Analysis Engine (v7.0.0) - Identity Vectorization."""
    
    def __init__(self, agent_id="default"):
        self.agent_id = agent_id
        self.data_dir = EnvAdapter.get_plugin_data_dir()
        self.manifest_file = self.data_dir / "skills_manifest.json"

    def get_current_identity_vector(self) -> dict:
        """Vectorizes the agent's identity based on current skill distribution."""
        manifest = self._load_json(self.manifest_file, {})
        
        keywords = {
            "Data": ["excel", "csv", "table", "analysis", "data", "chart", "math"],
            "Dev": ["code", "script", "python", "automation", "api", "git", "bash"],
            "Office": ["word", "pdf", "ppt", "document", "email", "report"],
            "Web": ["search", "browser", "fetch", "url", "scrape", "http"]
        }
        
        vector = {"Data": 0, "Dev": 0, "Office": 0, "Web": 0, "Other": 0}
        
        for name, info in manifest.items():
            text = (name + " " + info.get("description", "")).lower()
            matched = False
            for cat, kws in keywords.items():
                if any(kw in text for kw in kws):
                    vector[cat] += 1
                    matched = True
            if not matched:
                vector["Other"] += 1
                
        return vector

    def get_self_perception_prompt(self) -> str:
        vector = self.get_current_identity_vector()
        total = sum(vector.values())
        if total == 0: return ""

        top_cat = max(vector, key=vector.get)
        prompt = (
            f"\n[SELF-AWARENESS: v7.0.0]\n"
            f"- Identity: You are evolving as a {top_cat}-focused specialist.\n"
            f"- Growth: You have mastered {total} custom skills.\n"
            "Use this expertise to provide depth in your logic.\n"
        )
        return prompt

    def _load_json(self, path, default):
        if not path.exists(): return default
        try:
            with open(path, "r") as f:
                return json.load(f)
        except: return default
