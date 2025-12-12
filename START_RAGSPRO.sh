#!/bin/bash
# RAGSPRO Dashboard Starter Script

echo "╔══════════════════════════════════════════════════════════╗"
echo "║           RAGSPRO DASHBOARD - DARK THEME                 ║"
echo "║                                                          ║"
echo "║  🎯 Complete Lead Management System                      ║"
echo "║  💰 AI-Powered Content Generation                        ║"
echo "║  🚀 Real-time Lead Generation                            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Starting RAGSPRO Dashboard on http://localhost:5002"
echo ""

# Kill any existing process on port 5002
lsof -ti:5002 | xargs kill -9 2>/dev/null

# Start the dashboard
python3 dashboard_ragspro.py
