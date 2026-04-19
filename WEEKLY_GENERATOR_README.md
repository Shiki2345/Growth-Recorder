# 🚀 周报自动生成器使用指南

## 快速开始

### 1. 安装依赖

```bash
pip install anthropic PyPDF2
```

### 2. 配置环境变量

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "your-api-key-here"

# Linux/Mac
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 3. 运行脚本

```bash
# 基础用法
python weekly_summary_generator.py ./飞书文档.pdf "第4周"

# 简化用法（默认使用当前周数）
python weekly_summary_generator.py ./飞书文档.pdf
```

---

## 📋 功能详解

### 脚本做了什么

1. **读取PDF** → 提取文档内容
2. **调用Claude** → 按优先级生成结构化总结
3. **自动保存** → 更新周报文件、索引和日志

### 输出文件

- ✅ `每周总结/第X周总结.md` - 完整周报
- ✅ `每周日志索引.md` - 自动更新导航
- ✅ `已读文档日志.md` - 记录已处理的文档

### 总结优先级

| 优先级 | 内容 | 占比 |
|--------|------|------|
| 🥇 第一 | 个人思考、反思、洞察 | ~40% |
| 🥈 第二 | 方法论、框架、工具 | ~40% |
| 🥉 第三 | 工作任务、完成度 | ~20% |

---

## 🎯 工作流程

### 每周使用流程

**Step 1 - 准备文档** (你)
```
飞书写好周报 → 导出PDF到本地
```

**Step 2 - 生成总结** (自动化)
```bash
python weekly_summary_generator.py ./工作总结.pdf "第4周"
```

**Step 3 - 查看结果** (你)
```
打开 每周总结/第4周总结.md
确认内容 → 手动调整（如需要）
```

**Step 4 - 方法论沉淀** (手动)
```
从总结中提取关键方法论
添加到 产品方法论/ 文件夹
```

---

## ⚙️ 自定义配置

### 修改优先级权重

编辑 `weekly_summary_generator.py` 中的 `system_prompt`：

```python
总结优先级（重要程度）：
1. 个人思考 - 反思、洞察、学到的东西、思维转变（最优先）
2. 方法论 - 可复用的框架、工具、最佳实践
3. 工作任务 - 具体完成的工作、进度、产出物
```

### 修改输出目录

```python
# 第 53 行左右
summary_dir = base_path / "你的自定义目录"
```

### 修改模型或参数

```python
# 第 115 行左右
message = client.messages.create(
    model="claude-opus-4-6",  # 改这里
    max_tokens=4096,          # 或这里
    ...
)
```

---

## 🐛 常见问题

### Q: "ANTHROPIC_API_KEY not set"
**A:** 确保已设置环境变量。Windows 用户可以：
```powershell
# 临时设置（本次会话）
$env:ANTHROPIC_API_KEY = "sk-..."

# 永久设置（系统设置 → 环境变量）
```

### Q: "PyPDF2 not installed"
**A:** 脚本会自动尝试安装，或手动运行：
```bash
pip install PyPDF2
```

### Q: PDF 提取内容为空
**A:** 可能是 PDF 格式问题。尝试：
1. 确保 PDF 不是图片扫描版
2. 用其他 PDF 工具验证可读性
3. 复制文本内容到 `.txt` 文件，改用：
   ```python
   with open("summary.txt", "r", encoding="utf-8") as f:
       content = f.read()
   ```

### Q: Claude 响应格式错误
**A:** 脚本有容错机制，但如果仍有问题：
1. 检查 API key 是否有效
2. 增加 `max_tokens`（第 115 行）
3. 检查网络连接

---

## 📊 数据流向

```
飞书工作文档 (PDF)
        ↓
    [脚本读取]
        ↓
PDF 原始内容 (8000字符限制)
        ↓
    [Claude API]
        ↓
JSON 结构化总结
        ↓
   [格式转换]
        ↓
Markdown 周报
        ↓
    [保存]
        ↓
每周总结/第X周总结.md ✅
已读文档日志.md ✅
每周日志索引.md ✅
```

---

## 🚀 进阶用法

### 批量处理多个周报

创建 `batch_summary.sh`：

```bash
#!/bin/bash
python weekly_summary_generator.py "./周报/第1周.pdf" "第1周"
python weekly_summary_generator.py "./周报/第2周.pdf" "第2周"
python weekly_summary_generator.py "./周报/第3周.pdf" "第3周"
```

运行：
```bash
bash batch_summary.sh
```

### 定时自动执行 (Linux/Mac)

编辑 crontab：
```bash
crontab -e
```

每周五 17:00 自动生成：
```cron
0 17 * * 5 cd ~/project && python weekly_summary_generator.py ./工作总结.pdf "第$(date +%V)周"
```

### Windows 定时任务

1. 打开"任务计划程序"
2. 创建新任务
3. 操作：`python weekly_summary_generator.py ./工作总结.pdf "第4周"`
4. 触发器：每周五 17:00

---

## 📈 效果示例

**输入:** 飞书工作文档 (包含工作记录、想法、问题)

**输出:** 结构化周报，包含：
- ✨ 个人思考 - 你学到了什么
- 📚 方法论 - 可复用的框架
- 📋 工作任务 - 完成度和产出
- ⚠️ 问题复盘 - 根本原因和预防

---

## 💡 最佳实践

1. **定期整理** - 每周五下午运行脚本
2. **及时复盘** - 脚本生成后手动调整优化
3. **方法论沉淀** - 定期将亮点转移到方法论库
4. **知识积累** - 用 Memory 系统记录跨周的思想演进

---

## 🔗 相关文件

- `weekly_summary_generator.py` - 主脚本
- `每周总结/` - 周报存储目录
- `每周日志索引.md` - 总导航
- `已读文档日志.md` - 文档追踪
- `产品方法论/` - 方法论库

---

**Need help?** 检查脚本顶部的 docstrings 或修改 `max_tokens` 参数以获得更详细的输出。
