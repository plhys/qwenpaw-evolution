# -*- coding: utf-8 -*-
"""
Skill Manager v7.3.3 — Added CLI entry point for Non-MCP mode.
"""

import json
import logging
import os
import sys
import argparse
from pathlib import Path

# Add parent dir to sys.path to allow imports when run as script
sys.path.append(str(Path(__file__).parent.parent))

from lib.env_adapter import EnvAdapter

logger = logging.getLogger("qwenpaw.plugin.dream_engine.skill_manager")

_brain = None

def _get_brain():
    global _brain
    if _brain is None:
        try:
            from engine.brain import EvolutionBrain
            _brain = EvolutionBrain(agent_id="default")
        except Exception as e:
            # Try alternative import path
            try:
                from ..engine.brain import EvolutionBrain
                _brain = EvolutionBrain(agent_id="default")
            except:
                logger.error(f"Failed to init Brain: {e}")
                return None
    return _brain

def create_skill(name: str, description: str = "", content: str = "", 
                 test_code: str = "", reason: str = "CLI create") -> dict:
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
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    success, msg = brain.run_dream_logic()
    if success:
        return {"status": "success", "detail": msg}
    return {"status": "error", "reason": msg}

def approve_skill(name: str) -> dict:
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

def list_skills():
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    skills = []
    if brain.skills_dir.exists():
        for f in sorted(brain.skills_dir.glob("*.py")):
            skills.append({"name": f.stem, "path": str(f)})
    return {"status": "success", "skills": skills}

def get_evolution_timeline():
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    if brain.history_file.exists():
        with open(brain.history_file, "r") as f:
            history = json.load(f)
        return {"status": "success", "events": history}
    return {"status": "success", "events": []}

def archive_skill(name: str):
    brain = _get_brain()
    if brain is None: return {"status": "error", "reason": "Brain not initialized"}
    path = brain.skills_dir / f"{name}.py"
    if path.exists():
        path.unlink()
        return {"status": "success", "name": name}
    return {"status": "error", "reason": "Not found"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dream Engine CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Create command
    create_p = subparsers.add_parser("create")
    create_p.add_argument("--name", required=True)
    create_p.add_argument("--desc", default="")
    create_p.add_argument("--code", required=True)
    create_p.add_argument("--test", default="")
    create_p.add_argument("--reason", default="CLI Task")

    # Approve command
    approve_p = subparsers.add_parser("approve")
    approve_p.add_argument("--name", required=True)

    # Run Dream command
    subparsers.add_parser("run_dream")
    
    # List command
    subparsers.add_parser("list")

    args = parser.parse_args()

    if args.command == "create":
        print(json.dumps(create_skill(args.name, args.desc, args.code, args.test, args.reason)))
    elif args.command == "approve":
        print(json.dumps(approve_skill(args.name)))
    elif args.command == "run_dream":
        print(json.dumps(run_dream_cycle()))
    elif args.command == "list":
        print(json.dumps(list_skills()))
