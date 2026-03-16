---
name: url-reader
description: Fetch and read web content from URLs, converting to markdown format. Use when user sends a URL link and wants to: (1) Read the content of a webpage, (2) Scrape/extract content from a website, (3) Get URL content in markdown, (4) Open and parse a link. Trigger phrases include "读取链接", "抓取网页", "获取 URL 内容", "打开链接", "read this url", "fetch webpage", "get content from link".
---

# Url Reader

## Quick Start

Use the `mcp__web_reader__webReader` tool to fetch and convert web content to markdown.

## Usage

```yaml
Tool: mcp__web_reader__webReader
Required Parameters:
  - url: The website URL to fetch
Optional Parameters:
  - timeout: Request timeout in seconds (default: 20)
  - return_format: "markdown" or "text" (default: "markdown")
  - retain_images: Keep images true/false (default: true)
  - with_images_summary: Include images summary (default: false)
  - with_links_summary: Include links summary (default: false)
```

## Example

When user provides a URL like `https://example.com/article`:

1. Call `mcp__web_reader__webReader` with the URL
2. Return the markdown content to the user
3. Optionally summarize key points if content is long

## Notes

- Handles most websites including those requiring JavaScript rendering
- Preserves images and basic formatting
- Converts to LLM-friendly markdown output
- 20 second default timeout can be adjusted for slow sites
