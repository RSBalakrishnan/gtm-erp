FROM node:24-bookworm

# Install Python 3 + pip for agent skills
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Install OpenClaw CLI globally
RUN npm install -g openclaw@latest

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Create logs directory
RUN mkdir -p /app/logs

# Install Python dependencies for skills
RUN pip3 install --break-system-packages \
    requests \
    python-dotenv \
    gspread \
    oauth2client \
    google-auth \
    google-auth-oauthlib

# Expose gateway port
EXPOSE 18793

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:18793/health || exit 1

# Set environment
ENV OPENCLAW_CONFIG_PATH=/app/openclaw.json
ENV NODE_ENV=production

# Entry point
CMD ["openclaw", "gateway", "run", "--verbose"]
