---
name: archive-rag-project
description: "新能源发电企业工程档案归档标准化RAG系统(archive-rag),三层资产模型/V1纯结构化"
metadata: 
  node_type: memory
  type: project
  originSessionId: fdc2acaf-7d79-4885-a0c0-232414238999
---

用户在 `C:\Users\wqj85\archive-rag`（独立 git repo）做一个**工程档案归档标准化辅助系统**，服务归档技术负责人。目标：以标准模板 + 国标行标为依据，让新项目标准化归档。

核心设计（2026-07-24 定）：
- **三层知识资产**：Excel 卷内目录（骨架/确定性）+ Word 模板说明与样本（血肉/范本）+ 国标行标（依据/溯源）
- **两条数据流**：结构化流（V1-V2，无 LLM）+ 语义流（V3，有 LLM）
- **三阶段**：V1=生成清单+按类查范本+挂国标依据+固化模板（无 LLM，纯本地）；V2=缺项检查；V3=问答+内容合规
- **关键认知**：V1 瓶颈在业务梳理（模板固化 + 国标对照），不在代码；技术骨架先行、业务梳理并行

已确认决策：模板"借此次理清"（V1 承担固化）/ 输出 Excel / 国标全部新建（分批）/ 映射规则已明确（待用户给例子）。

当前阶段（2026-07-24）：spec v0.2 + V1 计划骨架已完成并 commit，等用户提供【脱敏真实 Excel 模板】+【3-5 个文件夹↔分类映射例子】后进入执行。
- spec：`docs/superpowers/specs/2026-07-24-archive-rag-design.md`
- plan：`docs/superpowers/plans/2026-07-24-archive-rag-v1.md`

方法论可参 [[ip-first-principles]]（第一性原理思维同源）。
