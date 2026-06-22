#!/usr/bin/env python3
"""Get more details on specific HK news topics."""
import urllib.request
import urllib.parse
import re

def fetch_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return ""

# Search for specific topics to get more details
def search_topic(query):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=zh-TW&num=5"
    content = fetch_url(url)
    results = []
    # Extract snippets and titles
    for m in re.finditer(r'<div[^>]*class="[^"]*VwiC3b[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if clean:
            results.append(clean)
    return results

topics = [
    "香港 H9N2 禽流感 兩歲男童 禾輋街市 2026",
    "香港 首個五年規劃 公眾諮詢 2026",
    "美伊達成協議 2026年6月",
    "5月訪港旅客 2026",
    "大家樂 業績 2026",
]

for topic in topics:
    print(f"\n=== {topic} ===")
    results = search_topic(topic)
    for r in results[:5]:
        print(f"  - {r[:300]}")
