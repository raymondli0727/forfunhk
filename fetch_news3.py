#!/usr/bin/env python3
"""Fetch more details on HK trending topics."""
import urllib.request
import urllib.parse
import re
import html

def fetch_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-HK,zh-TW;q=0.9,zh;q=0.8,en;q=0.7",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode('utf-8', errors='replace')

# Get more details on specific trending topics
topics = [
    ("地盤禁煙首日", "https://hk.news.yahoo.com/%E5%9C%B0%E7%9B%A4%E7%A6%81%E7%85%99%E9%A6%96%E6%97%A5-%E5%8B%9E%E5%B7%A5%E8%99%95%E5%B7%A1%E6%9F%A5-194%E8%99%95%E7%99%BC8%E5%BC%B5%E5%91%8A%E7%A5%A8-080351311.html"),
    ("Uber失物排行榜", "https://hk.news.yahoo.com/uber-%E5%8D%81%E5%A4%A7%E5%A4%B1%E7%89%A9-2026-070400150.html"),
    ("新皇崗口岸", "https://hk.news.yahoo.com/%E6%96%B0%E7%9A%87%E5%B4%97%E5%8F%A3%E5%B2%B8%E5%8D%B3%E5%B0%87%E9%96%8B%E9%80%9A-%E4%BA%A4%E9%80%9A%E7%B6%B2%E8%B7%AF%E5%9B%9B%E9%80%9A%E5%85%AB%E9%81%94-061200161.html"),
    ("長沙灣升降機急墜", "https://hk.news.yahoo.com/%E9%95%B7%E6%B2%99%E7%81%A3%E5%9C%B0%E7%9B%A4%E5%8D%87%E9%99%8D%E6%A9%9F%E6%80%A5%E5%A2%9C-2%E5%B7%A5%E4%BA%BA%E9%A0%AD%E5%82%B7%E9%80%81%E9%99%A2-092923770.html"),
]

for topic_name, url in topics:
    print(f"\n=== {topic_name} ===")
    try:
        content = fetch_url(url)
        # Try to get article body text
        paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
        text_parts = []
        for p in paras:
            text = re.sub(r'<[^>]+>', '', p).strip()
            text = html.unescape(text)
            if text and len(text) > 20:
                text_parts.append(text)
        # Print first few paragraphs
        for t in text_parts[:8]:
            print(f"  {t[:200]}")
            print()
    except Exception as e:
        print(f"  Error: {e}")

# Also get HK01 trending
print("\n\n=== HK01 熱門話題 ===")
try:
    content = fetch_url("https://www.hk01.com/")
    # Look for trending section
    # Find all h2/h3 with article links
    articles = re.findall(r'<a[^>]*href="https://www\.hk01\.com/[^"]*"[^>]*>.*?<span[^>]*>(.*?)</span>', content, re.DOTALL)
    if not articles:
        articles = re.findall(r'<a[^>]*href="/article/[^"]*"[^>]*>(.*?)</a>', content, re.DOTALL)
    seen = set()
    for a in articles[:25]:
        text = re.sub(r'<[^>]+>', '', a).strip()
        text = html.unescape(text)
        if text and len(text) > 5 and text not in seen:
            seen.add(text)
            print(f"  • {text[:100]}")
except Exception as e:
    print(f"  Error: {e}")
