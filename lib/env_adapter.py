import os
from pathlib import Path

class EnvAdapter:
    @staticmethod
    def get_base_dir():
        """Get QwenPaw environment base directory."""
        if "QWENPAW_HOME" in os.environ:
            return Path(os.environ["QWENPAW_HOME"])
        
        qwen_path = Path.home() / ".qwenpaw"
        if qwen_path.exists(): 
            return qwen_path
        
        return Path.cwd()

    @staticmethod
    def get_workspace_dir():
        """Get the current active workspace directory from environment."""
        if "QWENPAW_WORKING_DIR" in os.environ:
            return Path(os.environ["QWENPAW_WORKING_DIR"])
        
        # Fallback to base_dir / workspaces / default if not specified
        base = EnvAdapter.get_base_dir()
        default_ws = base / "workspaces" / "default"
        if default_ws.exists():
            return default_ws
            
        return Path.cwd()

    @staticmethod
    def get_plugin_data_dir():
        data_dir = EnvAdapter.get_base_dir() / "plugins" / "dream-evolution-engine" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir

    @staticmethod
    def get_evolved_skills_dir(agent_id: str = "default"):
        """Return the PRIVATE skill directory for a specific Agent to prevent cross-contamination."""
        skills_dir = EnvAdapter.get_plugin_data_dir() / "agent_skills" / agent_id
        skills_dir.mkdir(parents=True, exist_ok=True)
        return skills_dir

    @staticmethod
    def get_global_skills_dir():
        """Global skills shared across all agents."""
        global_dir = EnvAdapter.get_plugin_data_dir() / "shared_evolution"
        global_dir.mkdir(parents=True, exist_ok=True)
        return global_dir
