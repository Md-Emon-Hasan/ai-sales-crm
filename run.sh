#!/bin/bash

# AI Sales Campaign CRM - Quick Start Script
# This script sets up and runs the complete demo

set -e

echo "AI Sales Campaign CRM - Quick Start"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo " .env file not found!"
    echo ""
    echo "Creating .env from template..."
    cp .env.example .env
    echo ""
    echo " Please edit .env and add your GROQ_API_KEY"
    echo "   Get your key from: https://console.groq.com/keys"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if GROQ_API_KEY is set
source .env
if [ -z "$GROQ_API_KEY" ] || [ "$GROQ_API_KEY" = "your_groq_api_key_here" ]; then
    echo " GROQ_API_KEY not configured in .env"
    echo ""
    echo "Please edit .env and add your actual API key"
    echo "Get your key from: https://console.groq.com/keys"
    exit 1
fi

echo "Environment configured"
echo ""

# Build and start services
echo "Starting Docker services..."
docker-compose down -v 2>/dev/null || true
docker-compose up --build -d

echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check if services are running
if ! docker-compose ps | grep -q "Up"; then
    echo "Services failed to start"
    echo "Check logs with: docker-compose logs"
    exit 1
fi

echo "Services are running"
echo ""

# Trigger campaign
echo "Starting campaign processing..."
RESPONSE=$(curl -s -X POST http://localhost:8000/process-campaign)
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo ""

# Wait for processing
echo "Processing leads (this takes ~2 minutes)..."
sleep 120

# Check status
echo ""
echo "Campaign Status:"
curl -s http://localhost:8025 | python3 -m json.tool
echo ""

# Display results
echo ""
echo "=========================================="
echo "Campaign Complete!"
echo "=========================================="
echo ""
echo "View emails: http://localhost:8025"
echo "API docs: http://localhost:8000/docs"
echo "Status: http://localhost:8000/status"
echo ""
echo "Output files:"
echo "   - data/leads_enriched.csv (enriched lead data)"
echo "   - reports/*.md (campaign report)"
echo ""
echo "Check results:"
echo "   cat data/leads_enriched.csv"
echo "   cat reports/campaign_report_*.md"
echo ""
echo "Stop services:"
echo "   docker-compose down"
echo ""
echo "Demo ready for presentation!"