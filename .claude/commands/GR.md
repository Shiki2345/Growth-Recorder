---
description: 调用 growth-recorder skill（成长记录官）处理后续输入
---

调用 growth-recorder skill 处理用户本次的输入：$ARGUMENTS

按 skill 内部流程执行：
1. Step 0 模式识别（A 单文档提炼 / B 周总结），模糊时主动问
2. 按识别结果走对应分叉（A 部分步骤 / B 全 6 步）
3. 完成后按模式给简短汇报
