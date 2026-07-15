#!/usr/bin/env python3
"""Fetch Hong Kong trending topics from multiple sources."""
import urllib.request
import urllib.parse
import re
import json
import ssl

# Create SSL context that doesn't verify (for some sites)
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def fetch(url, timeout=15):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f""

# 1. Yahoo HK RSS
print("=" * 70)
print("YAHOO HK NEWS")
print("=" * 70)
content = fetch("https://hk.news.yahoo.com/rss/")
for m in re.finditer(r'<title>(.*?)</title>', content):
    t = m.group(1).strip()
    if t and 'Yahoo' not in t and len(t) > 5:
        print(f"  - {t}")

# 2. Bing News Search for HK trending
print("\n" + "=" * 70)
print("BING NEWS: 香港 2026年7月")
print("=" * 70)
for query in ["香港 最新消息 2026年7月", "世界盃 4強 西班牙 法國 2026", "香港 熱話 2026年7月15日"]:
    url = f"https://www.bing.com/news/search?q={urllib.parse.quote(query)}&setlang=zh-HK"
    content = fetch(url)
    titles = set()
    for m in re.finditer(r'<a[^>]*class="title"[^>]*>(.*?)</a>', content, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if clean and len(clean) > 10 and clean not in titles:
            titles.add(clean)
            print(f"  [{query[:10]}...] {clean}")
    for m in re.finditer(r'<a[^>]*data-title="([^"]*)"', content):
        t = m.group(1).strip()
        if t and len(t) > 10 and t not in titles:
            titles.add(t)
            print(f"  [{query[:10]}...] {t}")

# 3. RTHK RSS
print("\n" + "=" * 70)
print("RTHK NEWS (English RSS)")
print("=" * 70)
content = fetch("https://news.rthk.hk/rthk/en/rss/60")
for m in re.finditer(r'<title>(.*?)</title>', content):
    t = m.group(1).strip()
    if t and 'RTHK' not in t and len(t) > 5:
        print(f"  - {t}")

# 4. Try to search for Spain vs France result
print("\n" + "=" * 70)
print("BING NEWS: 西班牙 法國 世界盃 賽果")
print("=" * 70)
url = "https://www.bing.com/news/search?q=%E8%A5%BF%E7%8F%AD%E7%89%99+%E6%B3%95%E5%9C%8B+%E4%B8%96%E7%95%8C%E7%9B%83+%E8%B5%9B%E6%9E%9C&setlang=zh-HK"
content = fetch(url)
titles = set()
for m in re.finditer(r'<a[^>]*class="title"[^>]*>(.*?)</a>', content, re.DOTALL):
    clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if clean and len(clean) > 10 and clean not in titles:
        titles.add(clean)
        print(f"  - {clean}")
for m in re.finditer(r'<a[^>]*data-title="([^"]*)"', content):
    t = m.group(1).strip()
    if t and len(t) > 10 and t not in titles:
        titles.add(t)
        print(f"  - {t}")

# 5. HK01 RSS
print("\n" + "=" * 70)
print("HK01 RSS")
print("=" * 70)
content = fetch("https://www.hk01.com/rss/1")
for m in re.finditer(r'<title>(.*?)</title>', content):
    t = m.group(1).strip()
    if t and 'HK01' not in t and len(t) > 5:
        print(f"  - {t}")

# 6. Try Now News
print("\n" + "=" * 70)
print("NOW NEWS")
print("=" * 70)
content = fetch("https://news.now.com/home")
for m in re.finditer(r'<h[23][^>]*>(.*?)</h[23]>', content, re.DOTALL):
    clean = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    if clean and len(clean) > 10:
        print(f"  - {clean}")
