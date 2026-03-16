---
name: link-summarizer
description: Extract and summarize web content from URLs. Perfect for Feishu/Slack bots and messaging integrations. Use when: (1) User sends a URL and wants a summary, (2) Need to extract key points from a webpage, (3) Collaborative tools need to fetch link content, (4) Quick digest of articles/blog posts. Trigger phrases: "摘要这个链接", "总结这个网页", "获取链接摘要", "summarize this link", "what's this about", "TL;DR this URL".
---

# Link Summarizer

## Quick Start

When user sends a URL, automatically fetch content and generate a concise summary.

## Workflow

```
URL → webReader fetch → Content extraction → Summary → Formatted output
```

## Step 1: Fetch Content

Use `mcp__web_reader__webReader` to get the webpage content:

```yaml
url: <user_provided_url>
return_format: markdown
retain_images: false  # Disable images for faster fetching
timeout: 30
```

## Step 2: Generate Summary

Analyze the fetched content and extract:

| Element | Description |
|---------|-------------|
| **Title** | Article/page title |
| **Core Theme** | Main topic in one sentence |
| **Key Points** | 3-5 bullet points of main ideas |
| **Notable Quotes** | Memorable lines (if any) |
| **Action Items** | Any calls-to-action or conclusions |

## Step 3: Format Output

Return in a clean, messaging-friendly format:

```markdown
📎 **[Title]**

**核心内容：**
One-sentence summary.

**要点：**
• Point 1
• Point 2
• Point 3

**金句：**
> "Notable quote if applicable"

🔗 来源：[URL]
```

## Error Handling

| Error | Response |
|-------|----------|
| Invalid URL | ❌ "链接格式无效，请提供完整的 URL（包含 https://）" |
| Access denied | ⚠️ "该网站有访问限制，请尝试手动复制内容" |
| Timeout | ⏱️ "获取超时，请稍后重试" |
| Empty content | 📭 "页面内容为空或无法解析" |

## Platform-Specific Tips

### Feishu/飞书
- Keep summaries under 2000 characters (message limit)
- Use emoji for better readability
- Link back to original URL

### Slack
- Use message attachments for richer formatting
- Limit to 3-4 key points

### WeChat Work/企业微信
- Plain text format safest
- Avoid excessive markdown

## Notes

- For paywalled content (WSJ, Medium, etc.), note the limitation
- For login-required sites (WeChat articles, Zhihu), inform user
- Summary should be language-agnostic (match source or user preference)
- Preserve important data, numbers, and statistics
