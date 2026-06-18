#!/usr/bin/env bash
# Content generation script for ForFunHK
# This generates a new Cantonese article about a trending topic

set -e

DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M)
SLUG="trending-$DATE-$TIME"

# We use a Python script with calls to the Hermes tools
# The actual content generation is handled by the cron job's AI prompt
# This script just does the mechanics

echo "Cron trigger at $(date)"
echo "Next: web_search for trending topics → generate article → git commit → deploy"
echo "Script path: /root/forfunhk/"
