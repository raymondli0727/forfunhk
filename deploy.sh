#!/usr/bin/env bash
# Build and deploy script for ForFunHK
# This is called by the cron job after generating content

set -e
cd /root/forfunhk
npm run build 2>&1

# Source the Cloudflare token from .env and deploy with wrangler
set -a; source .env; set +a
npx --yes wrangler pages deploy dist --project-name forfunhk --branch main 2>&1

echo "✅ Deployed!"
