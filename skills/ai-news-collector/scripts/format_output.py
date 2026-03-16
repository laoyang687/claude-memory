#!/usr/bin/env python3
"""
Output Formatting Script for AI News

Converts collected news data into different formats (Markdown, Feishu-optimized, etc.)

Usage:
    python format_output.py --input news.json --format markdown
    python format_output.py --input news.json --format feishu --output news_feishu.md
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def format_markdown(news_items, detailed=True):
    """
    Format news items as standard Markdown.

    Args:
        news_items: List of structured news items
        detailed: Include full analysis section

    Returns:
        Markdown string
    """
    output = []

    # Header
    date_str = datetime.now().strftime("%Y-%m-%d")
    output.append(f"# AI News Digest - {date_str}\n\n")
    output.append(f"> **Collection Period**: {date_str}\n")
    output.append(f"> **Focus**: AI Application Cases\n")
    output.append(f"> **Total Items**: {len(news_items)}\n\n")
    output.append("---\n\n")

    # Highlights section
    output.append("## 🎯 Today's Highlights\n\n")
    output.append("[Summary of key trends will be added here]\n\n")
    output.append("---\n\n")

    # Featured applications
    output.append("## 📰 Featured Applications\n\n")

    for i, item in enumerate(news_items, 1):
        output.append(f"### {i}. {item.get('title', 'Untitled')}\n\n")

        output.append(f"**📅 Date**: {item.get('date', 'N/A')}\n")
        output.append(f"**🏢 Organization**: {item.get('organization', 'N/A')}\n")
        output.append(f"**🏭 Industry**: {item.get('industry', 'N/A')}\n")

        source = item.get('source', {})
        if isinstance(source, dict):
            output.append(f"**🔗 Source**: [{source.get('name', 'Source')}]({source.get('url', '#')})\n\n")
        else:
            output.append(f"**🔗 Source**: {source}\n\n")

        # Summary
        summary = item.get('summary', '')
        if summary:
            output.append(f"**Summary:**\n{summary}\n\n")

        # Application details
        if detailed and 'details' in item:
            details = item['details']
            output.append("**Application Details:**\n")
            if details.get('problem'):
                output.append(f"- **Problem**: {details['problem']}\n")
            if details.get('solution'):
                output.append(f"- **Solution**: {details['solution']}\n")
            if details.get('technology'):
                output.append(f"- **Technology**: {details['technology']}\n")
            if details.get('results'):
                output.append(f"- **Results**: {details['results']}\n")
            if details.get('scale'):
                output.append(f"- **Scale**: {details['scale']}\n")
            output.append("\n")

        # Significance
        if item.get('significance'):
            output.append(f"**Why It Matters:**\n{item['significance']}\n\n")

        output.append("---\n\n")

    # Analysis section (if detailed)
    if detailed:
        output.append(generate_analysis_section(news_items))

    # Footer
    output.append("---\n\n")
    output.append(f"**Prepared by**: AI News Collector\n")
    output.append(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    return "".join(output)


def format_feishu(news_items):
    """
    Format news items optimized for Feishu documents.

    Feishu supports:
    - Callout blocks (use > for highlights)
    - Tables
    - Headings with emojis
    - Bullet points and numbered lists

    Returns:
        Feishu-optimized Markdown string
    """
    output = []

    # Header with enhanced visual hierarchy
    date_str = datetime.now().strftime("%Y年%m月%d日")
    output.append(f"# 🤖 AI新闻摘要 - {date_str}\n\n")

    # Callout block for metadata
    output.append("> 📊 **本期统计**\n")
    output.append(f"> - 收集日期: {date_str}\n")
    output.append(f"> - 聚焦领域: AI应用案例\n")
    output.append(f"> - 新闻条数: {len(news_items)}条\n\n")

    # Highlights with callout
    output.append("## 🎯 今日焦点\n\n")
    output.append("> 💡 **关键趋势**\n")
    output.append("> [待补充：今日主要趋势总结]\n\n")

    # Table of contents
    output.append("## 📑 目录\n\n")
    for i, item in enumerate(news_items, 1):
        title = item.get('title', 'Untitled')
        output.append(f"{i}. [{title}](#应用案例-{i})\n")
    output.append("\n---\n\n")

    # Featured applications
    output.append("## 📰 应用案例详情\n\n")

    for i, item in enumerate(news_items, 1):
        # Anchor for TOC
        output.append(f"### 应用案例 {i}\n\n")

        # Title in callout for emphasis
        output.append(f"> ### {item.get('title', 'Untitled')}\n\n")

        # Metadata table
        output.append("| 项目 | 内容 |\n")
        output.append("|------|------|\n")
        output.append(f"| 📅 日期 | {item.get('date', 'N/A')} |\n")
        output.append(f"| 🏢 机构 | {item.get('organization', 'N/A')} |\n")
        output.append(f"| 🏭 行业 | {item.get('industry', 'N/A')} |\n")

        source = item.get('source', {})
        if isinstance(source, dict):
            output.append(f"| 🔗 来源 | [{source.get('name', 'Source')}]({source.get('url', '#')}) |\n")
        else:
            output.append(f"| 🔗 来源 | {source} |\n")
        output.append("\n")

        # Summary
        summary = item.get('summary', '')
        if summary:
            output.append(f"**📝 摘要**\n\n{summary}\n\n")

        # Application details in expandable format
        if 'details' in item:
            details = item['details']
            output.append("**🔍 应用详情**\n\n")

            if details.get('problem'):
                output.append(f"- **问题**: {details['problem']}\n")
            if details.get('solution'):
                output.append(f"- **方案**: {details['solution']}\n")
            if details.get('technology'):
                output.append(f"- **技术**: {details['technology']}\n")
            if details.get('results'):
                output.append(f"- **成果**: {details['results']}\n")
            if details.get('scale'):
                output.append(f"- **规模**: {details['scale']}\n")
            output.append("\n")

        # Significance in callout
        if item.get('significance'):
            output.append(f"> 💭 **意义**: {item['significance']}\n\n")

        output.append("---\n\n")

    # Analysis section with visual elements
    output.append("## 📊 数据分析\n\n")

    # Industry breakdown
    industry_count = {}
    for item in news_items:
        industry = item.get('industry', 'Other')
        industry_count[industry] = industry_count.get(industry, 0) + 1

    output.append("### 行业分布\n\n")
    output.append("| 行业 | 数量 | 占比 |\n")
    output.append("|------|------|------|\n")
    for industry, count in sorted(industry_count.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(news_items)) * 100
        output.append(f"| {industry} | {count} | {percentage:.1f}% |\n")
    output.append("\n")

    # Quick insights
    output.append("## 💡 快速洞察\n\n")
    output.append("> 📌 **关键发现**\n")
    output.append("> - [待补充：关键洞察1]\n")
    output.append("> - [待补充：关键洞察2]\n")
    output.append("> - [待补充：关键洞察3]\n\n")

    # Footer
    output.append("---\n\n")
    output.append(f"📅 **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    output.append(f"🤖 **生成工具**: AI News Collector\n")

    return "".join(output)


def generate_analysis_section(news_items):
    """Generate analysis section with statistics."""
    output = []

    output.append("## 📊 Analysis & Insights\n\n")

    # Industry breakdown
    industry_count = {}
    for item in news_items:
        industry = item.get('industry', 'Other')
        industry_count[industry] = industry_count.get(industry, 0) + 1

    output.append("### Industry Breakdown\n\n")
    output.append("| Industry | Count |\n")
    output.append("|----------|-------|\n")
    for industry, count in sorted(industry_count.items(), key=lambda x: x[1], reverse=True):
        output.append(f"| {industry} | {count} |\n")
    output.append("\n")

    # Technology trends
    tech_count = {}
    for item in news_items:
        if 'details' in item and 'technology' in item['details']:
            tech = item['details']['technology']
            if tech:
                tech_count[tech] = tech_count.get(tech, 0) + 1

    if tech_count:
        output.append("### Technology Trends\n\n")
        output.append("| AI Technology | Count |\n")
        output.append("|---------------|-------|\n")
        for tech, count in sorted(tech_count.items(), key=lambda x: x[1], reverse=True):
            output.append(f"| {tech} | {count} |\n")
        output.append("\n")

    return "".join(output)


def main():
    parser = argparse.ArgumentParser(description="Format AI news output")
    parser.add_argument("--input", required=True, help="Input JSON file with news data")
    parser.add_argument("--format", choices=["markdown", "feishu"], default="markdown",
                      help="Output format")
    parser.add_argument("--output", help="Output file path (optional)")
    parser.add_argument("--simple", action="store_true",
                      help="Simple format without detailed analysis")

    args = parser.parse_args()

    # Load input data
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Get news items (handle different JSON structures)
    if isinstance(data, list):
        news_items = data
    elif isinstance(data, dict) and 'items' in data:
        news_items = data['items']
    else:
        print("Error: Invalid input format. Expected list or dict with 'items' key.")
        return

    # Format output
    if args.format == "markdown":
        output = format_markdown(news_items, detailed=not args.simple)
    elif args.format == "feishu":
        output = format_feishu(news_items)

    # Write to file or print
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Output written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
