#!/usr/bin/env python3
"""Fetch Hong Kong trending topics."""
import urllib.request
import urllib.parse
import re
import html

def search_google(query, hl="zh-TW"):
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl={hl}&num=15"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='replace')
    return content

def extract_results(content):
    # Extract h3 titles
    results = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    titles = []
    for r in results:
        text = re.sub(r'<[^>]+>', '', r)
        text = html.unescape(text).strip()
        if text and len(text) > 5:
            titles.append(text)
    # Extract snippets/descriptions
    snippets = re.findall(r'<span[^>]*class="[^"]*aCOpRe[^"]*"[^>]*>(.*?)</span>', content, re.DOTALL)
    descs = []
    for s in snippets:
        text = re.sub(r'<[^>]+>', '', s)
        text = html.unescape(text).strip()
        if text and len(text) > 10:
            descs.append(text[:200])
    return titles, descs

keywords = [
    "香港今日熱話",
    "Hong Kong trending today",
    "香港網絡熱話",
    "香港新聞 今日",
    "香港 突發 新聞",
]

all_titles = []
for kw in keywords:
    try:
        print(f"\n=== Searching: {kw} ===")
        content = search_google(kw, "zh-TW" if "香港" in kw else "en")
        titles, descs = extract_results(content)
        for t in titles[:8]:
            if t not in all_titles:
                all_titles.append(t)
                print(f"  • {t}")
    except Exception as e:
        print(f"  Error: {e}")

print("\n\n=== ALL UNIQUE TOPICS ===")
for i, t in enumerate(all_titles, 1):
    print(f"{i}. {t}")
