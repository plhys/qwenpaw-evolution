# -*- coding: utf-8 -*-
"""
Skill Manager v7.1.0 — Bridge between MCP and EvolutionBrain.
Added: Approve Skill, Get Evolution Timeline, Run Dream Cycle.
"""

import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path

from .env_adapter import EnvAdapter

logger = logging.getLogger("qwenpaw.plugin.dream_engine.skill_manager")

_brain = None

def _get_brain():
    global _brain
    if _brain is None:
        try:
            try:
                from ..engine.brain import EvolutionBrain
            except (ImportError, ValueError):
                from engine.brain import EvolutionBrain
            _brain = EvolutionBrain(agent_id="default")
        except Exception as e:
            logger.error(f"Failed to init Brain: {e}")
            return None
    return _brain

def create_skill(name: str, description: str = "", content: str = "", 
                 test_code: str = "", reason: str = "MCP create") -> dict:
    """Create a new skill (v7.0.0+ defaults to Draft)."""
    name = name.lower().replace(" ", "-").replace("_", "-")
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}

    success, msg = brain.evolve_skill(
        name=name,
        description=description,
        python_code=content,
        test_code=test_code,
        reason=reason,
        is_draft=True 
    )

    if success:
        return {"status": "success", "name": name, "mode": "draft"}
    return {"status": "error", "reason": msg}

def run_dream_cycle() -> dict:
    """v7.1.0: Trigger backend-driven dream cycle logic."""
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    
    success, msg = brain.run_dream_logic()
    if success:
        return {"status": "success", "detail": msg}
    return {"status": "error", "reason": msg}

def approve_skill(name: str) -> dict:
    """Enterprise: Approve a draft skill to make it active."""
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    
    try:
        manifest = brain.cognition.manifest_file
        with open(manifest, "r+") as f:
            data = json.load(f)
            if name in data:
                data[name]["status"] = "active"
                f.seek(0); json.dump(data, f, indent=2); f.truncate()
                return {"status": "success", "name": name, "new_status": "active"}
            return {"status": "error", "reason": f"Skill '{name}' not found"}
    except Exception as e:
        return {"status": "error", "reason": str(e)}

def get_evolution_timeline() -> dict:
    """Returns the history of evolution including soul snapshots for visualization."""
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    
    if brain.history_file.exists():
        with open(brain.history_file, "r") as f:
            history = json.load(f)
        return {"status": "success", "events": history}
    return {"status": "success", "events": []}

def list_skills():
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    skills = []
    if brain.skills_dir.exists():
        for f in sorted(brain.skills_dir.glob("*.py")):
            skills.append({"name": f.stem, "path": str(f)})
    return {"status": "success", "skills": skills}

def archive_skill(name: str):
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    path = brain.skills_dir / f"{name}.py"
    if path.exists():
        path.unlink()
        return {"status": "success", "name": name}
    return {"status": "error", "reason": "Not found"}
