#!/bin/bash
# Project Cleanup Script - Organize everything properly

echo "🧹 Starting Project Cleanup..."

# Create archive folders
mkdir -p _archive/{old_tests,old_docs,old_scripts,old_templates}

# Move old test files
mv test_*.py _archive/old_tests/ 2>/dev/null
mv TEST_*.py _archive/old_tests/ 2>/dev/null

# Move old documentation
mv *_COMPLETE.md *_SUMMARY.md *_GUIDE.md *_STATUS.md _archive/old_docs/ 2>/dev/null
mv SYSTEM_*.md FINAL_*.md COMPLETE_*.md IMPLEMENTATION_*.md _archive/old_docs/ 2>/dev/null
mv *_CHECKLIST.md *_READY.md *_WORKING.md *_FIXED.md _archive/old_docs/ 2>/dev/null
mv *.txt _archive/old_docs/ 2>/dev/null

# Move old scripts
mv add_*.py fix_*.py implement_*.py create_*.py _archive/old_scripts/ 2>/dev/null
mv AUTO_*.py EXPORT_*.py GENERATE_*.py _archive/old_scripts/ 2>/dev/null
mv audit_system.py reset_generation.py _archive/old_scripts/ 2>/dev/null

# Move old templates
mv templates/dashboard.html templates/modern_dashboard.html templates/premium_dashboard.html _archive/old_templates/ 2>/dev/null
mv complete_ragspro_dashboard.html _archive/old_templates/ 2>/dev/null

# Keep only essential files
echo "✅ Cleanup complete!"
echo ""
echo "📁 Kept Essential Files:"
echo "   - dashboard.py (main entry)"
echo "   - dashboard_ragspro.py (backend)"
echo "   - templates/ragspro_dashboard.html (frontend)"
echo "   - README.md (main docs)"
echo "   - src/ (all modules)"
echo "   - config/ (settings)"
echo "   - data/ (leads)"
echo ""
echo "📦 Archived:"
ls -1 _archive/*/  2>/dev/null | wc -l
