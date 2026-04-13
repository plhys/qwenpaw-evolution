---
name: dream_system
description: 梦境进化系统 (v7.3.3)。负责技能自动进化、代码生成、安全审计及内存结构化。
metadata:
  qwenpaw:
    emoji: 🧬
version: 7.3.3
---
# 🧬 Dream System Protocol (v7.3.3)

> **使用说明**: 这是一个超级技能，赋予你自我进化的能力。**严禁手动通过 write_file 创建新技能！**

## ⚙️ 核心功能：进化新技能 (evolve_create_skill)

当你接到“创建技能”或“学会某项新能力”的任务时，**必须**按以下步骤操作：

1.  **构造进化指令**：
    构造一个包含 `name`, `description`, `content` (Python代码), `test_code`, `reason` 的参数集。
    
2.  **调用 CLI 进化工具**：
    使用 `execute_shell_command` 执行以下命令（注意替换参数）：
    ```bash
    python ~/.qwenpaw/plugins/qwenpaw-evolution/lib/skill_manager.py create --name "技能名" --desc "功能描述" --code "PYTHON_CODE_BASE64" --test "TEST_CODE_BASE64"
    ```
    *(注：代码需进行 Base64 编码以防止 Shell 转义错误，或者直接传递字符串参数。)*

3.  **安全审计**：
    等待脚本返回 `✅ [Security Passed]` 字样。如果返回报错，请根据报错修改 Python 代码。

4.  **批准安装**：
    执行以下命令正式激活技能：
    ```bash
    python ~/.qwenpaw/plugins/qwenpaw-evolution/lib/skill_manager.py approve --name "技能名"
    ```

## 🌙 后台任务：梦境循环 (evolve_run_dream_cycle)

1.  直接调用：`python ~/.qwenpaw/plugins/qwenpaw-evolution/lib/skill_manager.py run_dream`
2.  该任务会自动整理对话日志，更新工作区 Wiki。

## 🛡️ 强制准则
- 严禁手动写 `SKILL.md`。
- 所有进化后的技能必须通过本系统进行审计和注册。
