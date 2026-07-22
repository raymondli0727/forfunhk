#!/usr/bin/env python3
"""Fetch more HK trends."""
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

# Google News search for HK
for q in ["地盤禁煙 香港", "新皇崗口岸 開通", "Uber失物 2026 香港", "香港 熱話 今日"]:
    print(f"\n=== Google News: {q} ===")
    try:
        url = f"https://news.google.com/search?q={urllib.parse.quote(q)}&hl=zh-HK&gl=HK&ceid=HK:zh-Hant"
        content = fetch_url(url)
        # Extract article titles - try multiple patterns
        patterns = [
            r'<article[^>]*>.*?<a[^>]*>(.*?)</a>',
            r'class="[^"]*title[^"]*"[^>]*>(.*?)</',
            r'<h3[^>]*>(.*?)</h3>',
            r'<h4[^>]*>(.*?)</h4>',
        ]
        seen = set()
        for pat in patterns:
            items = re.findall(pat, content, re.DOTALL)
            for item in items:
                text = re.sub(r'<[^>]+>', '', item).strip()
                text = html.unescape(text)
                if text and len(text) > 10 and text not in seen:
                    seen.add(text)
                    print(f"  • {text[:150]}")
    except Exception as e:
        print(f"  Error: {e}")

# Also fetch from hk.on.cc / Oriental Daily
print("\n=== Oriental Daily ===")
try:
    content = fetch_url("https://hk.on.cc/hk/bkn/cnt/news/" + "index.html")
    titles = re.findall(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>', content, re.DOTALL)
    for t in titles[:10]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = html.unescape(text)
        if text and len(text) > 5:
            print(f"  • {text[:100]}")
except Exception as e:
    print(f"  Error: {e}")

# Try The Standard
print("\n=== The Standard ===")
try:
    content = fetch_url("https://www.thestandard.com.hk/")
    titles = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    for t in titles[:10]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = html.unescape(text)
        if text and len(text) > 5:
            print(f"  • {text[:100]}")
except Exception as e:
    print(f"  Error: {e}")
