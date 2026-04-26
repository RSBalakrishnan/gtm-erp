#!/bin/bash
# docker-setup.sh — GTM V4 Multi-Agent Gateway Setup
# Usage: ./docker-setup.sh

set -e

echo "🚀 GTM V4 Multi-Agent Gateway — Docker Setup"
echo "================================================"

# 1. Validate .env exists
if [ ! -f ".env" ]; then
    echo "❌ ERROR: .env file not found in project root."
    echo "   Copy from agents/gtm-v2/.env or create one with required variables."
    exit 1
fi

echo "✅ .env file found."

# 2. Validate openclaw.json exists
if [ ! -f "openclaw.json" ]; then
    echo "❌ ERROR: openclaw.json not found in project root."
    exit 1
fi

echo "✅ openclaw.json found."

# 3. Validate agent directories exist
AGENTS=("orchestrator" "researcher" "summarizer" "outreach-writer" "tracker")
for agent in "${AGENTS[@]}"; do
    if [ ! -d "agents/$agent" ]; then
        echo "❌ ERROR: Agent directory agents/$agent not found."
        exit 1
    fi
    echo "   ✅ Agent: $agent"
done

echo "✅ All 5 agent directories validated."

# 4. Create logs directory
mkdir -p logs

# 5. Build Docker image
echo ""
echo "🔨 Building Docker image (using cache to save data)..."
docker-compose build

# 6. Start the gateway
echo ""
echo "🐳 Starting GTM V4 Gateway container..."
docker-compose up -d

# 7. Wait for health check
echo ""
echo "⏳ Waiting for gateway to become healthy..."
sleep 10

# Check health
if curl -sf http://localhost:18793/health > /dev/null 2>&1; then
    echo "✅ Gateway is healthy!"
else
    echo "⚠️  Gateway may still be starting. Check with: docker-compose logs -f"
fi

echo ""
echo "================================================"
echo "🎯 GTM V4 Multi-Agent Gateway is running!"
echo ""
echo "   🌐 Gateway URL:  http://localhost:18793"
echo "   📊 Dashboard:    http://localhost:18793/dashboard"
echo "   📱 Telegram:     Connected (if bot token is set)"
echo ""
echo "   📋 Agents registered:"
for agent in "${AGENTS[@]}"; do
    echo "      • $agent"
done
echo ""
echo "   🔧 Useful commands:"
echo "      docker-compose logs -f          # View live logs"
echo "      docker-compose restart          # Restart gateway"
echo "      docker-compose down             # Stop gateway"
echo "      docker-compose build --no-cache # Rebuild image"
echo "================================================"
