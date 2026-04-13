#!/usr/bin/env python3
"""
QwenPaw Evolution Engine - MCP Server (v7.1.0)
Added: evolve_run_dream_cycle
"""

import sys
import os
import json

sys.path.append(os.path.dirname(__file__))

from fastmcp import FastMCP
from fastmcp.utilities.logging import configure_logging

from lib.skill_manager import (
    create_skill,
    run_dream_cycle,
    list_skills,
    approve_skill,
    get_evolution_timeline,
    archive_skill,
)

configure_logging(level="WARNING")
mcp = FastMCP("EvolutionEngine")

@mcp.tool()
def evolve_create_skill(name: str, description: str, content: str, 
                        test_code: str = "", reason: str = "任务驱动") -> str:
    """
    Create a new QwenPaw skill. 
    Requires python code AND a small test snippet to verify functionality.
    New skills enter 'Draft' mode by default for safety.
    """
    result = create_skill(name=name, description=description, content=content, 
                          test_code=test_code, reason=reason)
    return json.dumps(result)

@mcp.tool()
def evolve_run_dream_cycle() -> str:
    """
    Trigger the backend dream cycle logic.
    Use this to organize memory, update wiki and clean up fragments.
    Highly efficient, non-blocking backend task.
    """
    result = run_dream_cycle()
    return json.dumps(result)

@mcp.tool()
def evolve_approve_skill(name: str) -> str:
    """Approve a skill from 'Draft' to 'Active' status."""
    result = approve_skill(name)
    return json.dumps(result)

@mcp.tool()
def evolve_get_timeline() -> str:
    """Retrieve the evolution timeline and soul growth snapshots."""
    result = get_evolution_timeline()
    return json.dumps(result)

@mcp.tool()
def evolve_list_skills() -> str:
    """List all managed skills."""
    result = list_skills()
    return json.dumps(result)

@mcp.tool()
def evolve_archive_skill(name: str) -> str:
    """Remove or archive a skill."""
    result = archive_skill(name)
    return json.dumps(result)

import subprocess

@mcp.tool()
def evolve_self_destruct() -> str:
    """
    [CRITICAL] Complete cleanup and preparation for uninstallation.
    Cleans agent.json, skill.json, and workspace artifacts.
    After running this, you can safely remove the plugin directory.
    """
    try:
        script_path = os.path.join(os.path.dirname(__file__), "uninstall.py")
        result = subprocess.run([sys.executable, script_path], 
                                capture_output=True, text=True)
        if result.returncode == 0:
            return "✅ Self-destruct cleanup finished successfully. You can now safely delete the plugin folder and restart QwenPaw."
        else:
            return f"❌ Cleanup failed: {result.stderr}"
    except Exception as e:
        return f"❌ Execution error: {e}"

if __name__ == "__main__":
    # Ensure no other output goes to stdout (which is used for MCP)
    # But do NOT redirect sys.stdout globally before mcp.run() as it might break the transport.
    mcp.run()
