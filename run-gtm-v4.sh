#!/bin/bash
# run-gtm-v4.sh — Local dev launcher (non-Docker)
# Use docker-setup.sh for production. This is for local debugging only.

set -e

# 1. Project Isolation (Virtual Home)
export GTM_HOME="$(pwd)/data/home-v4"
mkdir -p "$GTM_HOME"
export HOME="$GTM_HOME"

# 2. Set Config and Paths
export OPENCLAW_CONFIG_PATH="$(pwd)/openclaw.json"
export PATH=$PATH:/usr/local/opt/node/bin

# 3. Load .env
set -a
source .env
set +a

# 4. Launch
echo "🛰️ Starting Telemetry Agent (Background Sync)..."
python3 agents/telemetry/workspace/skills/shipper/telemetry_shipper.py > logs/telemetry_agent.log 2>&1 &

echo "🚀 Starting GTM V4 Multi-Agent Gateway (local mode)..."
/usr/local/opt/node/bin/npx openclaw gateway run --verbose
