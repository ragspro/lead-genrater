#!/usr/bin/env python3
"""
Test India Seeding - Small sample to verify everything works
Tests: 2 cities × 3 categories = 6 queries
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Temporarily modify the seed script for testing
import seed_india_with_ai

# Override with small test data
seed_india_with_ai.INDIAN_CITIES = [
    "Delhi, India",
    "Mumbai, India",
]

seed_india_with_ai.INDIAN_CATEGORIES = [
    "dental clinic",
    "software company",
    "restaurant",
]

print("""
╔══════════════════════════════════════════════════════════╗
║              TEST RUN - INDIA SEEDING                    ║
║                                                          ║
║  🧪 Testing with 2 cities × 3 categories = 6 queries    ║
║  ⚡ Quick test to verify everything works                ║
╚══════════════════════════════════════════════════════════╝
""")

# Run the seeding
seed_india_with_ai.seed_india_database()
