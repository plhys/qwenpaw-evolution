import logging
import json

# 使用更具体的 logger 名称避免冲突
logger = logging.getLogger("qwenpaw.plugin.dream_engine.messenger")

class Messenger:
    """Enhanced product-level UI Bridge (v7.2.2) - Supports Native QwenPaw UI Cards."""
    
    def __init__(self, api=None):
        self.api = api

    def _broadcast(self, card_text: str):
        """Sends the message to the UI if API is available, otherwise logs it."""
        if self.api and hasattr(self.api, "send_message"):
            try:
                # Use the plugin API to send a proactive message to the current channel
                self.api.send_message(message=card_text)
            except Exception as e:
                logger.error(f"Failed to send UI message: {e}")
        
        # Always log for traceability
        logger.info(f"\n[UI NOTIFICATION]\n{card_text}\n")

    def evolution_start_card(self, name: str, reason: str):
        """Show the proactive motivation card."""
        card = (
            f"🧬 **[DREAM ENGINE] 进化启动**\n"
            f"--- \n"
            f"🔹 **目标技能**: `{name}`\n"
            f"🧠 **进化动机**: *{reason}*\n"
            f"\n⏳ **代码构建中... 正在启动 AST 安全审计护盾**"
        )
        self._broadcast(card)

    def success_card_pro(self, name: str, description: str, stats: dict):
        """High-transparency success card with optimized Markdown."""
        card = (
            f"✅ **[能力进化成功！]**\n"
            f"--- \n"
            f"✨ **技能名称**: `{name}`\n"
            f"📝 **核心功能**: {description}\n"
            f"🛡️ **审计状态**: `PASSED (AST Safe)`\n"
            f"📊 **规模**: {stats.get('lines', 0)} 行代码\n"
            f"\n--- \n"
            f"💡 **下一步**: 该技能已存为草稿，请对我说“**批准安装 {name}**”来正式启用它。"
        )
        self._broadcast(card)

    def dream_digest_card(self, audit_summary: str, items_updated: int):
        """Audit log card."""
        card = (
            f"🌙 **[梦境循环简报]**\n"
            f"--- \n"
            f"🛡️ **审计摘要**: {audit_summary}\n"
            f"♻️ **知识同步**: 已更新 `{items_updated}` 项认知条目\n"
            f"\n*系统认知已刷新，进化引擎运行良好。*"
        )
        self._broadcast(card)

    def warning(self, text: str, detail: str = ""):
        card = f"⚠️ **[DREAM ENGINE 警告]**\n{text}"
        if detail:
            card += f"\n> 详情: {detail}"
        self._broadcast(card)
