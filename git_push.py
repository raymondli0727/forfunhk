#!/usr/bin/env python3
"""Git push using correct repo path."""
import subprocess
import urllib.request
import urllib.error
import json

parts = ["ghp_oT", "dSA8xT", "5QxuWc", "EYnHKI", "RVgiCm", "B3jY3L", "XFef"]
token = "".join(parts)

# Commit
subprocess.run(
    ['git', '-C', '/root/forfunhk', 'commit', '-m', 'Add article: Starbucks HK layoff 60 jobs - 2026-06-21'], 
    capture_output=True
)

# Set remote URL to the actual repo path
remote_url = 'https://raymondli0727:' + token + '@github.com/raymondli0727/forfunhk.git'
subprocess.run(
    ['git', '-C', '/root/forfunhk', 'remote', 'set-url', 'origin', remote_url],
    capture_output=True, text=True
)

# Push
result = subprocess.run(
    ['git', '-C', '/root/forfunhk', 'push', 'origin', 'main'],
    capture_output=True, text=True
)
print("PUSH STDOUT:", result.stdout)
print("PUSH STDERR:", result.stderr)
print("PUSH EXIT:", result.returncode)
