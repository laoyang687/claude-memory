#!/usr/bin/env python3
"""
AI News Search and Collection Script

This script provides helper functions for searching and organizing AI news.
Note: Claude has built-in WebSearch capability, so this script is optional.
Use it if you want to save search results or automate the process.

Usage:
    python search_and_collect.py --date today --focus applications
"""

import argparse
from datetime import datetime, timedelta
import json


def generate_search_queries(focus="applications", date_range="today", industry=None):
    """
    Generate optimized search queries for AI news.

    Args:
        focus: Type of news to find (applications, research, products, industry)
        date_range: Time period (today, week, month)
        industry: Specific industry to focus on (healthcare, finance, retail, etc.)

    Returns:
        List of search query strings
    """
    base_queries = []

    # Date specification
    date_str = ""
    if date_range == "today":
        date_str = datetime.now().strftime("%Y-%m-%d")
    elif date_range == "week":
        week_ago = datetime.now() - timedelta(days=7)
        date_str = f"{week_ago.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}"

    # Focus-specific queries
    if focus == "applications":
        base_queries = [
            f"AI applications {date_str}",
            f"artificial intelligence use cases {date_str}",
            f"AI implementation examples {date_str}",
            f"machine learning applications {date_str}",
            f"AI deployment {date_str}",
        ]
    elif focus == "products":
        base_queries = [
            f"AI product launch {date_str}",
            f"new AI tool {date_str}",
            f"AI software release {date_str}",
        ]
    elif focus == "industry":
        base_queries = [
            f"AI industry news {date_str}",
            f"enterprise AI adoption {date_str}",
            f"AI business impact {date_str}",
        ]

    # Add industry-specific queries
    if industry:
        industry_queries = [
            f"{industry} AI applications {date_str}",
            f"AI in {industry} {date_str}",
            f"{industry} artificial intelligence case study {date_str}",
        ]
        base_queries.extend(industry_queries)

    return base_queries


def filter_results(results, criteria):
    """
    Filter search results based on criteria.

    Args:
        results: List of news items (dict with title, url, summary, date)
        criteria: Filter criteria (dict with keys: min_relevance, exclude_keywords, etc.)

    Returns:
        Filtered list of news items
    """
    filtered = []

    exclude_keywords = criteria.get("exclude_keywords", [
        "research paper", "arxiv", "prediction", "will transform"
    ])

    for item in results:
        title_lower = item.get("title", "").lower()
        summary_lower = item.get("summary", "").lower()

        # Check for exclusion keywords
        if any(keyword in title_lower or keyword in summary_lower for keyword in exclude_keywords):
            continue

        # Add more filtering logic here
        # - Check for application indicators
        # - Verify recency
        # - Score relevance

        filtered.append(item)

    return filtered


def structure_news_item(raw_item):
    """
    Structure a raw news item into the template format.

    Args:
        raw_item: Dict with raw news data (title, url, summary, source, date)

    Returns:
        Structured dict ready for template
    """
    structured = {
        "title": raw_item.get("title", "Untitled"),
        "date": raw_item.get("date", datetime.now().strftime("%Y-%m-%d")),
        "organization": extract_organization(raw_item),
        "industry": extract_industry(raw_item),
        "source": {
            "name": raw_item.get("source", "Unknown"),
            "url": raw_item.get("url", "")
        },
        "summary": raw_item.get("summary", ""),
        "details": {
            "problem": "",  # To be filled by analysis
            "solution": "",
            "technology": extract_ai_technology(raw_item),
            "results": "",
            "scale": ""
        },
        "significance": ""
    }

    return structured


def extract_organization(item):
    """Extract organization name from news item."""
    # Simple heuristic - look for common patterns
    text = f"{item.get('title', '')} {item.get('summary', '')}"

    # Common patterns: "Company announces...", "At Company,...", etc.
    # This is a placeholder - actual implementation would use NER or more sophisticated parsing

    return "Unknown Organization"


def extract_industry(item):
    """Identify industry/sector from news content."""
    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()

    industry_keywords = {
        "healthcare": ["hospital", "medical", "health", "clinical", "patient"],
        "finance": ["bank", "financial", "trading", "payment", "fintech"],
        "retail": ["retail", "e-commerce", "shopping", "store", "consumer"],
        "manufacturing": ["manufacturing", "factory", "production", "supply chain"],
        "technology": ["software", "cloud", "platform", "tech company"],
    }

    for industry, keywords in industry_keywords.items():
        if any(keyword in text for keyword in keywords):
            return industry.title()

    return "Other"


def extract_ai_technology(item):
    """Identify type of AI technology mentioned."""
    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()

    tech_keywords = {
        "Large Language Model": ["llm", "gpt", "language model", "chatgpt", "claude"],
        "Computer Vision": ["computer vision", "image recognition", "object detection", "cv"],
        "Natural Language Processing": ["nlp", "natural language", "text analysis"],
        "Machine Learning": ["machine learning", "ml model", "predictive model"],
        "Generative AI": ["generative ai", "generation", "synthesis", "stable diffusion"],
    }

    for tech, keywords in tech_keywords.items():
        if any(keyword in text for keyword in keywords):
            return tech

    return "AI/ML"


def generate_markdown_output(news_items, template_path=None):
    """
    Generate markdown output from structured news items.

    Args:
        news_items: List of structured news items
        template_path: Path to template file (optional)

    Returns:
        Markdown formatted string
    """
    output = []

    # Header
    output.append(f"# AI News Digest - {datetime.now().strftime('%Y-%m-%d')}\n")
    output.append(f"> **Total Items**: {len(news_items)}\n")
    output.append("---\n")

    # News items
    for i, item in enumerate(news_items, 1):
        output.append(f"### {i}. {item['title']}\n")
        output.append(f"**📅 Date**: {item['date']}\n")
        output.append(f"**🏢 Organization**: {item['organization']}\n")
        output.append(f"**🏭 Industry**: {item['industry']}\n")
        output.append(f"**🔗 Source**: [{item['source']['name']}]({item['source']['url']})\n\n")

        if item['summary']:
            output.append(f"**Summary**: {item['summary']}\n\n")

        output.append("---\n\n")

    return "".join(output)


def main():
    parser = argparse.ArgumentParser(description="AI News Search Helper")
    parser.add_argument("--date", choices=["today", "week", "month"], default="today",
                      help="Date range for search")
    parser.add_argument("--focus", choices=["applications", "products", "industry"],
                      default="applications", help="Focus area")
    parser.add_argument("--industry", type=str, help="Specific industry to focus on")
    parser.add_argument("--output", type=str, help="Output file path")

    args = parser.parse_args()

    # Generate search queries
    queries = generate_search_queries(
        focus=args.focus,
        date_range=args.date,
        industry=args.industry
    )

    print("Generated search queries:")
    for i, query in enumerate(queries, 1):
        print(f"{i}. {query}")

    print("\n" + "="*50)
    print("Note: This script generates search queries.")
    print("Use Claude's WebSearch tool to execute these queries.")
    print("Then use the structure_news_item() function to format results.")
    print("="*50)

    # Save queries to file if output specified
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "parameters": vars(args),
                "queries": queries
            }, f, indent=2, ensure_ascii=False)
        print(f"\nQueries saved to: {args.output}")


if __name__ == "__main__":
    main()
