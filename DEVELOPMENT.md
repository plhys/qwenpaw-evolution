# 🛠️ QwenPaw Evolution 开发逻辑与架构文档

本文档详细介绍了梦境进化引擎的内部实现逻辑、模块协作方式以及核心算法。

---

## 1. 总体架构：双径系统 (Hot & Cold Path)

引擎采用了独特的“双径”设计模型：

### 🔥 Hot Path (热路径：实时进化)
*   **触发时机**：用户在对话中显式要求，或 Agent 识别到当前环境缺少工具。
*   **实现载体**：`mcp_server.py` 暴露的 `evolve_create_skill` 工具。
*   **逻辑流**：
    1.  LLM 生成 Python 代码。
    2.  调用 MCP 工具，进入 `EvolutionBrain`。
    3.  `SecurityShield` 进行 AST 审计（拒绝危险指令）。
    4.  `DependencyManager` 正则提取 `import`，调用 `pip` 自动安装缺失库。
    5.  代码编译测试 (`compile`)。
    6.  原子化写入磁盘并注册到 `CognitionManifest`。
    7.  通过 `Messenger` 反馈 UI 卡片。

### 🌙 Cold Path (冷路径：梦境循环)
*   **触发时机**：闲时或用户调用 `dream_system` 技能。
*   **职责**：
    - **整理**：将 `memory/` 下的碎片聊天摘要（Compact files）提取事实，合并到 `memory/wiki/` 结构化知识库。
    - **维护**：更新 Wiki 索引，建立双向链接。
    - **衰减**：识别长时间未使用的、重要性低的记忆文件，移动到 `archive/`。
    - **技能审计**：清理报错技能，合并功能重复的技能。

---

## 2. 核心模块逻辑实现

### 🛡️ 安全审计 (Security Shield)
*   **逻辑**：不使用简单的字符串匹配，而是利用 `ast.parse` 将代码转为语法树。
*   **实现**：遍历树节点，识别具有潜在风险的系统调用。
*   **设计哲学**：宽松授权（Power-user focused）。仅拦截 `rm -rf /` 等自毁级指令，保留 99% 的灵活性。

### 🧠 灵魂与意识 (Soul & Cognition)
*   **意识注入 (Awareness)**：`CognitionEngine` 维护一个 JSON 清单。每次对话开始时，插件会将这个清单格式化为“你学会了以下技能：...”的 Prompt，强制注入 Agent 的上下文。
*   **身份建模 (Identity)**：`SoulEngine` 会遍历所有已进化技能的描述。
    - 使用 `Counter` 统计关键词（如 "excel", "chart" -> Data-focused）。
    - 动态生成一段自我评价词（如：“你已经进化为一个专注于数据分析的专家”）。
    - 这种反馈回路让 Agent 的角色设定随着技能增加而自动偏移。

### 📦 依赖管理器 (Dependency Manager)
*   **挑战**：AI 编写的代码经常使用环境里没有的第三方库。
*   **逻辑**：使用正则表达式 `^\s*(?:import|from)\s+([a-zA-Z0-9_]+)` 扫描代码顶部。
*   **自愈**：通过 `importlib.metadata` 检查包是否已安装。若缺失，调用 `subprocess` 执行 `pip install`。
*   **超时控制**：修复版增加了 60s 硬超时，防止网络卡顿导致整个 Agent 进程卡死。

### 🔌 插件引导 (Bootstrap)
*   **逻辑**：在 `on_startup` 阶段检查工作区标记。
*   **自适应配置**：
    - 它会自动读取 `agent.json`。
    - 探测当前的 Python 解释器绝对路径 (`sys.executable`)。
    - 自动拼装 MCP 配置项并注入，无需用户手动编辑 JSON。

---

## 3. 核心流程伪代码

```python
# 技能进化核心伪代码
def evolve_skill(code):
    # 1. 静态安全检查
    if not shield.audit(code):
        return "Security block"
    
    # 2. 自动解决依赖
    missing_deps = extract_imports(code)
    pip_install(missing_deps)
    
    # 3. 环境验证
    try:
        compile(code)
    except SyntaxError:
        return "Fix your code"
        
    # 4. 持久化
    save_to_disk(code)
    
    # 5. 意识唤醒
    cognition.register(new_skill)
    return "Evolution success"
```

---

## 4. 修复与优化说明 (v6.9.0)

1.  **通信协议保护**：将 `print` 全部替换为 `logging`。在 MCP (stdio) 模式下，任何意外的 `stdout` 输出都会破坏 JSON-RPC 消息帧，导致连接断开。
2.  **异步兼容性**：QwenPaw 的 Hook 逐渐向异步迁移，`async def on_startup` 确保了在高并发或长任务初始化时不阻塞网关。
3.  **路径动态化**：消灭了所有 `~/.qwenpaw` 类的硬编码路径，改用 `Path(__file__)` 向上推导，支持任何安装路径。
