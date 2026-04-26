#!/bin/bash
# run-gtm-v2.sh

# 1. Project Isolation (Virtual Home)
# Overriding HOME ensures the buggy 'exec' tool cannot find the symlinked ~/.openclaw
# as per Issue #29736. This forces a real directory for state/approvals.
export GTM_HOME="/Users/administrator/Documents/gtm/agents/gtm-v2/data/home"
mkdir -p "$GTM_HOME"
export HOME="$GTM_HOME"

# 2. Set Config and Paths
export OPENCLAW_CONFIG_PATH="/Users/administrator/Documents/gtm/agents/gtm-v2/openclaw.json"
export PATH=$PATH:/usr/local/opt/node/bin

# 3. Launch
/usr/local/opt/node/bin/npx openclaw gateway run --verbose