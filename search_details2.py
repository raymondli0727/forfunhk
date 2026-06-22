#!/usr/bin/env python3
"""Get details from specific HK news article pages."""
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

# Let's try to access specific news sites
# 1. Try bing search for H9N2 news
def bing_news_search(query):
    url = f"https://www.bing.com/news/search?q={urllib.parse.quote(query)}&setlang=zh-HK"
    content = fetch_url(url)
    results = []
    for m in re.finditer(r'<a[^>]*class="title"[^>]*>(.*?)</a>', content, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if clean and len(clean) > 10:
            results.append(clean)
    # Alternative pattern
    if not results:
        for m in re.finditer(r'<a[^>]*data-title="([^"]*)"', content):
            t = m.group(1).strip()
            if t and len(t) > 10:
                results.append(t)
    return results

# Try to access RTHK Chinese page
def rthk_chinese():
    content = fetch_url("https://news.rthk.hk/rthk/ch/latest-news.htm")
    results = []
    for m in re.finditer(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', content, re.DOTALL):
        href = m.group(1)
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if text and len(text) > 10 and 'rthk' in href.lower():
            results.append((href, text))
    return results

print("=== RTHK Chinese Latest News ===")
items = rthk_chinese()
for href, text in items[:20]:
    print(f"  {text}")
    print(f"    {href}")

print("\n\n=== Bing News: H9N2 ===")
for r in bing_news_search("H9N2 禽流感 香港 男童"):
    print(f"  - {r}")

print("\n=== Bing News: 美伊協議 ===")
for r in bing_news_search("美伊 協議 2026"):
    print(f"  - {r}")

print("\n=== Bing News: 五年規劃 ===")
for r in bing_news_search("香港 五年規劃"):
    print(f"  - {r}")

print("\n=== Bing News: 訪港旅客 ===")
for r in bing_news_search("訪港旅客 5月 2026"):
    print(f"  - {r}")

print("\n=== Bing News: 香港今日 ===")
for r in bing_news_search("香港今日新聞"):
    print(f"  - {r}")
