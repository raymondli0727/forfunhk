#!/usr/bin/env python3
"""Git push using token from environment."""
import subprocess
import sys
import os

token = os.environ.get("GH_TOKEN", "")
if not token:
    print("ERROR: GH_TOKEN environment variable not set")
    sys.exit(1)

repo = "/root/forfunhk"
remote_url = f"https://raymondli0727:{token}@github.com/raymondli0727/forfunhk.git"
subprocess.run(["git", "-C", repo, "remote", "set-url", "origin", remote_url], capture_output=True)

result = subprocess.run(["git", "-C", repo, "push", "origin", "main"], capture_output=True, text=True)
print("PUSH STDOUT:", result.stdout.strip())
print("PUSH STDERR:", result.stderr.strip())
print("PUSH EXIT:", result.returncode)
sys.exit(result.returncode)
