#!/usr/bin/env python3
"""Fetch Hong Kong trending topics from HK news sites."""
import urllib.request
import urllib.parse
import re
import html
import json

def fetch_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-HK,zh-TW;q=0.9,zh;q=0.8,en;q=0.7",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode('utf-8', errors='replace')

# Try HK01 (one of HK's biggest news sites)
try:
    print("=== HK01 熱門新聞 ===")
    content = fetch_url("https://www.hk01.com/")
    # Find article titles
    # HK01 uses specific patterns
    titles = re.findall(r'<h3[^>]*class="[^"]*"[^>]*>.*?<span[^>]*>(.*?)</span>', content, re.DOTALL)
    if not titles:
        titles = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    for t in titles[:15]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = html.unescape(text)
        if text and len(text) > 5:
            print(f"  • {text[:100]}")
except Exception as e:
    print(f"  Error HK01: {e}")

# Try Yahoo News HK
try:
    print("\n=== Yahoo News HK ===")
    content = fetch_url("https://hk.news.yahoo.com/")
    titles = re.findall(r'<h3[^>]*>.*?<a[^>]*href="[^"]*"[^>]*>(.*?)</a>', content, re.DOTALL)
    if not titles:
        titles = re.findall(r'class="[^"]*title[^"]*"[^>]*>.*?<a[^>]*>(.*?)</a>', content, re.DOTALL)
    if not titles:
        # Try another pattern
        titles = re.findall(r'<a[^>]*class="[^"]*"[^>]*>.*?<span[^>]*>(.*?)</span>', content, re.DOTALL)
    if not titles:
        titles = re.findall(r'class="[^"]*[Tt]itle[^"]*"[^>]*>(.*?)</', content, re.DOTALL)
    for t in titles[:15]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = html.unescape(text)
        if text and len(text) > 5:
            print(f"  • {text[:100]}")
except Exception as e:
    print(f"  Error Yahoo: {e}")

# Try Now News
try:
    print("\n=== Now News ===")
    content = fetch_url("https://news.now.com/home")
    titles = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    for t in titles[:15]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = html.unescape(text)
        if text and len(text) > 5:
            print(f"  • {text[:100]}")
except Exception as e:
    print(f"  Error Now: {e}")

# Try to get HK trending topics from Google Trends
try:
    print("\n=== Google Trends Hong Kong (Daily) ===")
    content = fetch_url("https://trends.google.com.tw/trends/trendingsearches/daily?geo=HK&hl=zh-TW")
    titles = re.findall(r'<div[^>]*class="[^"]*title[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL)
    for t in titles[:15]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = html.unescape(text)
        if text and len(text) > 3:
            print(f"  • {text[:100]}")
except Exception as e:
    print(f"  Error Trends: {e}")

# Also try The Standard / SCMP for English trending topics
try:
    print("\n=== SCMP Top Stories ===")
    content = fetch_url("https://www.scmp.com/")
    titles = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    for t in titles[:10]:
        text = re.sub(r'<[^>]+>', '', t).strip()
        text = html.unescape(text)
        if text and len(text) > 5:
            print(f"  • {text[:100]}")
except Exception as e:
    print(f"  Error SCMP: {e}")

print("\n\n=== DONE ===")
