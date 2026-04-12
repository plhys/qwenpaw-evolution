import json
import logging
import uuid
import threading
from datetime import datetime
from pathlib import Path
try:
    from ..lib.env_adapter import EnvAdapter
except (ImportError, ValueError):
    from lib.env_adapter import EnvAdapter

logger = logging.getLogger("qwenpaw.DreamEngine.Lab")
_lab_lock = threading.Lock() # Global Lock for history synchronization

class SkillLab:
    """Product-level Lab management with thread-safe operations (v6.3.1)."""
    
    def __init__(self, agent_id="default"):
        self.agent_id = agent_id
        self.skills_dir = EnvAdapter.get_evolved_skills_dir(agent_id)
        self.data_dir = EnvAdapter.get_plugin_data_dir()
        self.history_file = self.data_dir / f"history_{agent_id}.json"
        self.quarantine_dir = self.data_dir / "quarantine"
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

    def get_full_report(self):
        """Generate a stable, detailed laboratory status report."""
        with _lab_lock:
            history = self._load_history()
            active_skills = [f.stem for f in self.skills_dir.glob("*.py")]
            blocked_skills = [f.stem for f in self.quarantine_dir.glob("*.py")]
            
            return {
                "status": "Healthy",
                "metrics": {
                    "active_count": len(active_skills),
                    "quarantine_count": len(blocked_skills),
                    "total_evolutions": len(history)
                },
                "active_skills": active_skills,
                "quarantine_list": blocked_skills,
                "recent_history": history[-5:][::-1]
            }

    def rollback_skill(self, name: str):
        """Thread-safe rollback of an evolved skill."""
        skill_path = self.skills_dir / f"{name}.py"
        if skill_path.exists():
            try:
                skill_path.unlink()
                self._log_event("rollback", name, "User-initiated cleanup.")
                return True, f"Skill '{name}' has been successfully removed."
            except Exception as e:
                return False, f"Rollback failed: {e}"
        return False, f"Skill '{name}' not found."

    def quarantine_skill(self, name: str, code: str, reason: str):
        """Quarantine dangerous skills instead of deleting them."""
        q_path = self.quarantine_dir / f"{name}.py"
        with open(q_path, "w", encoding="utf-8") as f:
            f.write(f"# Quarantine: {reason}\n\n{code}")
        self._log_event("quarantine", name, reason)

    def _load_history(self):
        if not self.history_file.exists(): return []
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except: return []

    def _log_event(self, event_type, name, detail):
        """Log a new event into the history with stable IDs and timestamps."""
        with _lab_lock:
            history = self._load_history()
            history.append({
                "id": str(uuid.uuid4())[:8],
                "type": event_type,
                "name": name,
                "detail": detail,
                "timestamp": datetime.now().isoformat()
            })
            with open(self.history_file, "w") as f:
                json.dump(history, f, indent=2)
