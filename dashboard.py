#!/usr/bin/env python3
"""
RAGSPRO DASHBOARD - Main Entry Point
This is the DEFAULT dashboard that always runs
Port: 5002
"""

# Import everything from the main RAGSPRO dashboard
from dashboard_ragspro import *

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           RAGSPRO DASHBOARD - DEFAULT ENTRY              ║
    ║                                                          ║
    ║  🎯 Complete Lead Management System                      ║
    ║  💰 AI-Powered Content Generation                        ║
    ║  🚀 Real-time Lead Generation                            ║
    ║                                                          ║
    ║  This is your DEFAULT dashboard - always use this!       ║
    ╚══════════════════════════════════════════════════════════╝
    
    🚀 Dashboard running at: http://localhost:5002
    📊 Open your browser and start generating premium leads!
    
    ⚡ Quick Commands:
       - Generate Leads: Click "Generate" button
       - View Leads: Automatically loaded
       - Search: Use search box
       - Export: Click "CSV" button
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5002)
