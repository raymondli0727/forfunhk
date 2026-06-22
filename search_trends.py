#!/usr/bin/env python3
"""Search for Hong Kong trending topics using different sources."""
import urllib.request
import urllib.parse
import re
import json
import sys

def google_search(query):
    """Search Google and extract result titles and snippets."""
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=zh-TW&num=10"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='replace')
        
        # Extract search result titles
        results = []
        # Look for h3 tags (standard search results)
        for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL):
            clean = re.sub(r'<[^>]+>', '', m.group(1))
            clean = clean.strip()
            if clean and len(clean) > 5:
                results.append(clean)
        
        # Also try to get snippets
        snippets = []
        for m in re.finditer(r'<div[^>]*class="[^"]*VwiC3b[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL):
            clean = re.sub(r'<[^>]+>', '', m.group(1))
            clean = clean.strip()
            if clean and len(clean) > 10:
                snippets.append(clean)
        
        return results, snippets
    except Exception as e:
        return [], [f"Error: {e}"]

def bing_search(query):
    """Search Bing for HK trending topics."""
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&setlang=zh-HK"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-HK,zh;q=0.9,en;q=0.8',
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='replace')
        
        results = []
        for m in re.finditer(r'<h2[^>]*><a[^>]*>(.*?)</a>', content, re.DOTALL):
            clean = re.sub(r'<[^>]+>', '', m.group(1))
            clean = clean.strip()
            if clean and len(clean) > 5:
                results.append(clean)
        return results
    except Exception as e:
        return [f"Error: {e}"]

def rthk_news():
    """Get RTHK news headlines."""
    try:
        url = "https://news.rthk.hk/rthk/en/rss/60"  # HK news RSS
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='replace')
        headlines = []
        for m in re.finditer(r'<title>(.*?)</title>', content):
            t = m.group(1).strip()
            if t and 'RTHK' not in t:
                headlines.append(t)
        return headlines[:10]
    except:
        return []

# Search queries
queries = [
    "香港今日熱話",
    "Hong Kong trending today",
    "香港網絡熱話 2026",
    "香港新聞 今日",
]

all_results = []
for q in queries:
    titles, snippets = google_search(q)
    for t in titles:
        all_results.append(("google", q, t))
    for s in snippets[:3]:
        all_results.append(("google_snippet", q, s[:200]))

print("=" * 80)
print("SEARCH RESULTS - HONG KONG TRENDING TOPICS")
print("=" * 80)

for source, query, text in all_results[:50]:
    print(f"[{source}] ({query}) {text}")
    print()

# Also try RTHK
print("\n--- RTHK News ---")
for h in rthk_news():
    print(f"  - {h}")

print("\n--- Bing Search ---")
for q in queries[:2]:
    for r in bing_search(q):
        print(f"  [{q}] {r}")
