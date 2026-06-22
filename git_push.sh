#!/bin/bash
# GitHub push script
# Token passed via STDIN

cd /root/forfunhk

# Read token from stdin
read TOKEN

# Commit
git commit -m "Add article: H9N2 bird flu case in 2-year-old child (June 20)" 2>&1

# Set remote
git remote set-url origin "https://forfunhk-bot:${TOKEN}@github.com/forfunhk/forfunhk.git" 2>&1

# Push
git push origin main 2>&1
echo "EXIT_CODE: $?"
