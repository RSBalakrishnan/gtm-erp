#!/bin/bash
# run-gtm-v4.sh — Local dev launcher (non-Docker)
# Use docker-setup.sh for production. This is for local debugging only.

set -e

# 1. Project Isolation (Virtual Home)
export GTM_HOME="/Users/administrator/Documents/gtm/data/home-v4"
mkdir -p "$GTM_HOME"
export HOME="$GTM_HOME"

# 2. Set Config and Paths
export OPENCLAW_CONFIG_PATH="/Users/administrator/Documents/gtm/openclaw.json"
export PATH=$PATH:/usr/local/opt/node/bin

# 3. Load .env
set -a
source /Users/administrator/Documents/gtm/.env
set +a

# 4. Launch
echo "🚀 Starting GTM V4 Multi-Agent Gateway (local mode)..."
/usr/local/opt/node/bin/npx openclaw gateway run --verbose
