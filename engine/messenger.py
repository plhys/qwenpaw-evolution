import logging

# 使用更具体的 logger 名称避免冲突
logger = logging.getLogger("qwenpaw.plugin.dream_engine.messenger")

class Messenger:
    """Enhanced product-level UI Bridge (v6.3.2) - Refactored to use standard logging."""
    
    def __init__(self, agent=None):
        self.agent = agent

    def info(self, text: str):
        logger.info(f"[Dream Engine] {text}")

    def evolution_start_card(self, reason: str):
        """Show the proactive motivation card."""
        card = (
            f"💡 **[进化动机触发]**\n"
            f"--- \n"
            f"识别到改进空间：\n"
            f"> *{reason}*\n"
            f"\n🚀 **引擎正为您构建定制化工具...**"
        )
        logger.info(card)

    def thinking(self, text: str, progress: int = None):
        p_bar = ""
        if progress is not None:
            filled = progress // 10
            p_bar = f" [{progress}%]"
        logger.info(f"⏳ [Dream Engine] {text}{p_bar}")

    def success_card_pro(self, name: str, description: str, code: str, stats: dict):
        """High-transparency success card with optimized Markdown."""
        code_preview = code if len(code) < 400 else code[:400] + "\n# ... (rest hidden)"
        
        card = (
            f"✨ **[新能力解锁！]**\n"
            f"--- \n"
            f"🔹 **技能名称**: `{name}`\n"
            f"📝 **功能描述**: {description}\n"
            f"📊 **统计信息**: {stats['size_kb']:.2f} KB | {stats['lines']} 行\n"
            f"\n🔍 **代码预览**:\n"
            f"```python\n{code_preview}\n```\n"
            f"--- \n"
            f"💡 **操作指南**: 对我说“帮我{description}”以调用它。"
        )
        logger.info(card)

    def lab_report_card(self, metrics: dict, active_skills: list, quarantined: list):
        """Standardized lab dashboard (Rich Markdown)."""
        active_str = ", ".join([f"`{s}`" for s in active_skills]) if active_skills else "_无_"
        quarantine_str = ", ".join([f"`{s}`" for s in quarantined]) if quarantined else "_无_"
        
        report = (
            f"🧪 **[技能实验室报告]**\n"
            f"--- \n"
            f"| 状态 | 指标 | 技能清单 |\n"
            f"| :--- | :--- | :--- |\n"
            f"| ✅ **活跃** | {metrics['active_count']} | {active_str} |\n"
            f"| ⚠️ **隔离** | {metrics['quarantine_count']} | {quarantine_str} |\n"
            f"| 📉 **总量** | {metrics['total_evolutions']} | 系统运行稳定 |\n"
            f"\n*提示：回复“回滚 [技能名]”以移除特定技能。*"
        )
        logger.info(report)

    def dream_digest_card(self, audit_summary: str, items_updated: int, memory_saved: float):
        """Audit log card."""
        card = (
            f"🌙 **[梦境审计简报]**\n"
            f"--- \n"
            f"🛡️ **摘要**: {audit_summary}\n"
            f"♻️ **Wiki**: 已同步 {items_updated} 项词条\n"
            f"📉 **内存**: 优化节省了 {memory_saved:.1f} KB\n"
            f"\n*引擎已完成自我修复，认知库状态良好。*"
        )
        logger.info(card)

    def warning(self, text: str, detail: str = ""):
        msg = f"⚠️ [Dream Engine] {text}"
        if detail:
            msg += f" (原因: {detail})"
        logger.warning(msg)

    def _send_to_ui(self, message: str):
        """Deprecated in favor of standard logging."""
        logger.info(message)
