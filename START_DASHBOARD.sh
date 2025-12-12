#!/bin/bash
# DEFAULT DASHBOARD STARTER - Always use this!

echo "╔══════════════════════════════════════════════════════════╗"
echo "║           RAGSPRO DASHBOARD - STARTING...                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing process on port 5002
lsof -ti:5002 | xargs kill -9 2>/dev/null

# Start the DEFAULT dashboard
python3 dashboard.py
