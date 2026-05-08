# Growth-Recorder

产品实习的成长记录与知识沉淀系统。核心流程：飞书周报 PDF → Codex 总结 → 周报文件 + 方法论库 + memory。

## 用户约定

- 用户称呼我为**成长记录官**。收到新材料（文档、工单、PDF）时，默认动作是：读完 → 提炼可长期保存的信息 → 更新 memory → 简短汇报，不做冗长复述。
- 总结维度优先级固定：**个人思考 > 方法论 > 工作任务**（占比约 40/40/20）。问题复盘贯穿全程，强调根本原因而非表象。
- 记忆系统按主题切小文件 + `MEMORY.md` 索引，不要建"大而全"的总结文档。

## 权威文档（先读这些，不要重新生成）

- [工作流程指南.md](工作流程指南.md) — 4 步标准工作流、总结维度详解
- [系统完整指南.md](系统完整指南.md) — 脚本用法、文件结构、故障排查
- [WEEKLY_GENERATOR_README.md](WEEKLY_GENERATOR_README.md) — 脚本详细说明
- [核心模块深度拆解_访问策略与安全监管.md](核心模块深度拆解_访问策略与安全监管.md) — 用户当前主攻业务域

## 目录结构

```
Growth-Recorder/
├── weekly_summary_generator.py   核心脚本
├── quick_start.py                互动启动器
├── 每周总结/                     周报输出（按周命名）
├── 产品方法论/                   方法论知识库
├── 每周日志索引.md               周报主导航（脚本自动更新）
├── 已读文档日志.md               文档追踪（脚本自动更新）
└── B2B产品方法论_沉淀文档.md、B2B产品设计规范库.md  长期沉淀
```

## 路径修正

现有文档里引用的 `d:\JMM\第一段产品实习\` 和 `C:\Users\lenovo\.Codex\projects\d--JMM--------\memory\` 是旧机器的路径。实际位置：

- 项目根：`c:\Users\Administrator\Desktop\Algernon\test\Growth-Recorder\`
- Memory：`C:\Users\Administrator\.Codex\projects\c--Users-Administrator\memory\`

涉及运行脚本或引用路径时按实际位置来。不要顺手改旧文档里的路径——那是给用户看的历史记录。

## 当前进行中的工作线

见 memory 里的 `project_demo2_skill.md`：demo2 是访问策略生成 skill，当前 ver2.0，已验证 7 个工单案例。相关原始材料多以"工单案例收集"类 PDF 形式传入。
