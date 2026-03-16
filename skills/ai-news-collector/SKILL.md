---
name: ai-news-collector
description: AI news collection and curation assistant. Use when users want to find, collect, or organize AI news and updates, especially focusing on AI application cases. Trigger phrases include "find AI news", "collect AI updates", "latest AI applications", or "AI industry news".
---

# AI News Collector

This skill helps collect, filter, and organize AI news with a focus on practical AI application cases.

## Workflow

When a user requests AI news collection, follow these steps:

### 1. Search for AI News

Use WebSearch to find recent AI news from multiple sources:

```
Search queries to try:
- "AI applications [today's date]"
- "artificial intelligence use cases [today's date]"
- "AI implementation examples [today's date]"
- "machine learning applications [today's date]"
```

Cast a wide net across:
- Technology news sites (TechCrunch, VentureBeat, The Verge)
- AI-focused publications (MIT Technology Review, AI News)
- Chinese AI media (机器之心, AI科技评论, 量子位)
- Industry reports and case studies

### 2. Filter for AI Application Cases

Focus on news that demonstrates **practical AI applications**. Prioritize:

✅ **Include:**
- Real-world AI implementations in companies/industries
- Specific use cases with measurable outcomes
- Product launches using AI technology
- Case studies showing AI solving business problems
- Industry adoption of AI tools

❌ **Exclude:**
- Pure research papers without applications
- Generic AI hype or predictions
- Funding announcements without product details
- Opinion pieces without concrete examples

See [references/filtering_guidelines.md](references/filtering_guidelines.md) for detailed criteria.

### 3. Structure the Information

For each relevant news item, extract:
- **Title**: Clear, descriptive headline
- **Source**: Publication name and URL
- **Date**: Publication date
- **Summary**: 2-3 sentence overview
- **Application Details**: What problem does it solve? What industry? What results?
- **Key Takeaway**: Why this matters

### 4. Format the Output

Generate output in the user's preferred format:

#### Markdown Format (Default)

Use the template in [assets/news_template.md](assets/news_template.md):

```markdown
# AI News Digest - [Date]

## 🎯 Today's Highlights
[1-2 sentence overview of key trends]

## 📰 Application Cases

### [Title]
**Source**: [Publication] | [Date]
**Industry**: [Industry/Domain]
**Link**: [URL]

[2-3 sentence summary]

**Application Details**:
- Problem: [What problem was solved]
- Solution: [How AI was applied]
- Results: [Measurable outcomes if available]

---

[Repeat for each news item]

## 📊 Summary
- Total items: X
- Top industries: [List]
- Key trends: [Brief analysis]
```

#### Feishu Document Format

For Feishu output:
1. Generate the Markdown version first
2. Optimize formatting for Feishu:
   - Use Feishu-compatible headings
   - Add colored callout blocks for highlights
   - Include table of contents
   - Add emoji for visual hierarchy

Note: Direct Feishu API integration requires authentication. The skill outputs Feishu-optimized markdown that can be copy-pasted into Feishu docs.

### 5. Additional Features

**Search Customization**: If user specifies:
- Time range: "this week", "last 3 days", etc.
- Specific domains: "healthcare AI", "finance AI", etc.
- Regions: "China AI news", "US AI news", etc.

Adjust search queries accordingly.

**Source Recommendations**: See [references/news_sources.md](references/news_sources.md) for curated list of reliable AI news sources.

## Tips for Best Results

1. **Be specific in searches**: Include date ranges and specific domains for better results
2. **Verify credibility**: Prioritize established tech publications and official company announcements
3. **Focus on substance**: Look for concrete details, not just buzzwords
4. **Provide context**: Explain why each application case is significant
5. **Stay current**: AI news becomes outdated quickly; focus on recent content

## Example Usage

**User**: "帮我找今天的AI新闻"

**Response**:
1. Search for today's AI application news
2. Filter for concrete use cases
3. Structure findings using the template
4. Output as Markdown (or Feishu format if specified)

**User**: "整理一下本周医疗AI的应用案例"

**Response**:
1. Search for this week's healthcare AI news
2. Filter for medical/healthcare applications specifically
3. Structure and output results
