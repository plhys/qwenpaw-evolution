import os
import sys
import logging
import json
import threading
from pathlib import Path
from .env_adapter import EnvAdapter

logger = logging.getLogger("qwenpaw.DreamEngine.Bootstrap")
_init_lock = threading.Lock()

class BootstrapManager:
    """The Product-level Zero-Config Initializer (v6.4.0)."""
    
    @staticmethod
    def initialize():
        """Ensure the entire ecosystem is ready for immediate use."""
        with _init_lock:
            # 1. Get base directories
            base_dir = EnvAdapter.get_base_dir()
            plugin_data_dir = EnvAdapter.get_plugin_data_dir()
            skills_dir = EnvAdapter.get_evolved_skills_dir()
            quarantine_dir = plugin_data_dir / "quarantine"
            
            # 2. Ensure all directories exist
            dirs = [plugin_data_dir, skills_dir, quarantine_dir]
            for d in dirs:
                if not d.exists():
                    logger.info(f"Creating directory: {d}")
                    d.mkdir(parents=True, exist_ok=True)
            
            # 3. Initialize critical data files with safe defaults
            # History File
            history_file = plugin_data_dir / "history_default.json"
            if not history_file.exists():
                with open(history_file, "w") as f:
                    json.dump([], f)
                    
            # Cognition Manifest
            manifest_file = plugin_data_dir / "skills_manifest.json"
            if not manifest_file.exists():
                with open(manifest_file, "w") as f:
                    json.dump({}, f)
                    
            logger.info("Dream Evolution Engine: Bootstrap complete. Zero-config ready.")
            return True
