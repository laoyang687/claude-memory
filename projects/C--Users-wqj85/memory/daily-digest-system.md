---
name: daily-digest-system
description: 每日信息早报系统：27个精选公众号RSS→Windows计划任务7:30自动抓→Claude总结，判断力的结构化输入端
metadata: 
  node_type: memory
  type: project
  originSessionId: e7bc209b-2f3a-47d9-88f0-8a0b645d7164
---

老杨的「每日信息早报」系统，2026-07-27 搭建。

**位置**：`C:\Users\wqj85\DailyDigest\`
- `my_digest.opml` — 27个精选源（6方向：AI模型公司/AI独立实践/商业科技/财经判断/个人成长/创业思考）
- `fetch_digest.ps1` — 抓取脚本，每源最新3篇，生成 today.md + digest_日期.md
- Windows 计划任务 `DailyDigest`，每日 07:30 以用户 wqj85 身份自动跑，`-StartWhenAvailable` 开机补跑，`-WindowStyle Hidden` 不弹窗

**每天用法**：早上打开 Claude 说「看今天的早报」→ 读 today.md → 按赛道总结成 AI前沿/商业判断/财经/内容灵感。

**为什么**：呼应用户的 [[money-5yr-shift]] —— 未来5年赚钱靠"判断力+信任+系统"，信息差已死。这套系统是判断力的**结构化输入端**：不被动刷375个源（=信息过载=放弃），而是精选27个+AI总结，把信息变成可行动的判断。也呼应文章作者洞察"用户先选来源，AI再帮你筛选"，以及个人IP [[ip-first-principles]] 的一致性。

**技术坑（重要）**：PS 5.1 读无 BOM 的 .ps1 会按 GBK 解码中文，导致中文字符串错位、引号失配、连锁语法崩。脚本必须存 **UTF-8 with BOM**（`[System.IO.File]::WriteAllText($p, $c, [System.Text.Encoding]::UTF8)`）。RSS 中文 feed 用 `HttpWebRequest` + `StreamReader(UTF8)` 按字节解码最稳（`Invoke-WebRequest` 对无 charset header 的响应会误按 Latin1 解，出现乱码）。

**来源**：精选自 BestBlogs 的 375 个公众号 OPML（github.com/ginobefun/BestBlogs），RSS 托管在 wechat2rss.bestblogs.dev（作者自建实例，比公网 wechat2rss 稳）。全量 375 个 OPML 备份在 `Downloads\bestblogs_wechat_opml.opml`，想扩源就从这里挑。
