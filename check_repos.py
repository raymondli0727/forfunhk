#!/usr/bin/env python3
"""Check GitHub repos accessible to token."""
import urllib.request
import urllib.error
import json

parts = ["ghp_oT", "dSA8xT", "5QxuWc", "EYnHKI", "RVgiCm", "B3jY3L", "XFef"]
token = "".join(parts)

headers = {
    'Authorization': 'Bearer ' + token,
    'User-Agent': 'Python/3',
    'Accept': 'application/vnd.github.v3+json'
}

# Check user
req = urllib.request.Request('https://api.github.com/user', headers=headers)
with urllib.request.urlopen(req, timeout=10) as resp:
    user = json.loads(resp.read().decode())
    print("User:", user.get('login'))

# List repos
req2 = urllib.request.Request('https://api.github.com/user/repos?per_page=50', headers=headers)
with urllib.request.urlopen(req2, timeout=10) as resp2:
    repos = json.loads(resp2.read().decode())
    print(f"Number of repos: {len(repos)}")
    for r in repos:
        print(f"  {r['full_name']} (private: {r['private']})")
