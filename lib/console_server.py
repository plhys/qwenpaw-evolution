import threading
import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .env_adapter import EnvAdapter

logger = logging.getLogger("qwenpaw.DreamEngine.Console")

app = FastAPI(title="Dream Evolution Lab Console")

# Setup templates (in a real scenario, these would be in a templates folder)
# For simplicity in this environment, we'll embed a basic template
class ConsoleServer:
    """The Sidecar Web Console for Dream Evolution Engine (v6.7.0)."""
    
    def __init__(self, port=8080):
        self.port = port
        self.thread = None

    def start(self):
        """Start the FastAPI server in a background thread."""
        self.thread = threading.Thread(
            target=lambda: uvicorn.run(app, host="127.0.0.1", port=self.port, log_level="error"),
            daemon=True
        )
        self.thread.start()
        logger.info(f"Web Console started on http://127.0.0.1:{self.port}")

@app.get("/", response_class=HTMLResponse)
async def read_dashboard():
    # Fetch real data from the Lab
    from ..engine.lab import SkillLab
    lab = SkillLab("default") # Base report
    report = lab.get_full_report()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dream Evolution Lab</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; background: #1e1e1e; color: #d4d4d4; padding: 20px; }}
            .card {{ background: #252526; border-radius: 8px; padding: 15px; margin-bottom: 15px; border: 1px solid #3c3c3c; }}
            h1 {{ color: #007acc; }}
            .tag {{ background: #007acc; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; }}
            .skill-item {{ border-bottom: 1px solid #3c3c3c; padding: 10px 0; }}
            pre {{ background: #000; padding: 10px; border-radius: 4px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>🐾 Dream Evolution Lab Console</h1>
        <div class="card">
            <h2>📊 系统状态</h2>
            <p>活跃技能: {report['metrics']['active_count']} | 隔离区: {report['metrics']['quarantine_count']}</p>
        </div>
        
        <div class="card">
            <h2>✅ 活跃技能清单</h2>
            {"".join([f'<div class="skill-item"><code>{s}</code> <span class="tag">Active</span></div>' for s in report['active_skills']])}
        </div>

        <div class="card">
            <h2>📜 进化历史</h2>
            {"".join([f'<div class="skill-item"><b>{h["name"]}</b> - {h["detail"]} <br><small>{h["timestamp"]}</small></div>' for h in report['recent_history']])}
        </div>
        
        <p style="font-size: 12px; color: #666;">* 此控制台仅在本地运行 (localhost)，确保您的隐私安全。</p>
    </body>
    </html>
    """
    return html_content
