#!/usr/bin/env python3
"""Get Hong Kong trending news from HK01, RTHK, and other sources."""
import urllib.request
import urllib.parse
import re
import json

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
        return f""

# 1. HK01 - hk01.com latest news
def hk01_latest():
    content = fetch_url("https://www.hk01.com/")
    results = []
    # Try to find article titles
    for m in re.finditer(r'<h[23][^>]*>(.*?)</h[23]>', content, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if clean and len(clean) > 8 and len(clean) < 100:
            results.append(clean)
    return results[:15]

# 2. RTHK news
def rthk_latest():
    content = fetch_url("https://news.rthk.hk/rthk/ch/latest-news.htm")
    results = []
    for m in re.finditer(r'<a[^>]*href="[^"]*"[^>]*>(.*?)</a>', content, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if clean and len(clean) > 10:
            results.append(clean)
    return results[:15]

# 3. Yahoo News HK
def yahoo_hk():
    content = fetch_url("https://hk.news.yahoo.com/")
    results = []
    for m in re.finditer(r'<h[23][^>]*>(.*?)</h[23]>', content, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if clean and len(clean) > 10:
            results.append(clean)
    return results[:15]

# 4. Now News
def now_news():
    content = fetch_url("https://news.now.com/home")
    results = []
    for m in re.finditer(r'<h[23][^>]*>(.*?)</h[23]>', content, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if clean and len(clean) > 10:
            results.append(clean)
    return results[:15]

# 5. Try to get HK01 RSS
def hk01_rss():
    content = fetch_url("https://www.hk01.com/rss/1")
    results = []
    for m in re.finditer(r'<title>(.*?)</title>', content):
        t = m.group(1).strip()
        if t and 'HK01' not in t and len(t) > 5:
            results.append(t)
    return results[:10]

print("=" * 60)
print("HONG KONG LATEST NEWS - TRENDING TOPICS")
print("=" * 60)

print("\n--- HK01 Latest ---")
for i, t in enumerate(hk01_latest()[:10], 1):
    print(f"{i}. {t}")

print("\n--- RTHK News ---")
for i, t in enumerate(rthk_latest()[:10], 1):
    print(f"{i}. {t}")

print("\n--- Yahoo HK News ---")
for i, t in enumerate(yahoo_hk()[:10], 1):
    print(f"{i}. {t}")

print("\n--- HK01 RSS ---")
for i, t in enumerate(hk01_rss()[:10], 1):
    print(f"{i}. {t}")
