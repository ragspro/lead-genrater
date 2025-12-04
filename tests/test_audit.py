"""
Property-based tests for system audit
Feature: system-integration-polish
"""

import pytest
from hypothesis import given, strategies as st
from pathlib import Path
import ast
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from audit_system import CodeAuditor


class TestAuditProperties:
    """Property-based tests for code audit"""
    
    def test_property_1_all_python_files_have_valid_syntax(self):
        """
        Feature: system-integration-polish, Property 1: All Python files have valid syntax
        Validates: Requirements 1.1
        
        For any Python file in the src/ directory, running Python's AST parser 
        should successfully parse the file without syntax errors.
        """
        auditor = CodeAuditor()
        syntax_errors = auditor.audit_syntax()
        
        # Property: No syntax errors should exist
        assert len(syntax_errors) == 0, f"Found syntax errors: {syntax_errors}"
    
    def test_property_2_all_imports_resolve_correctly(self):
        """
        Feature: system-integration-polish, Property 2: All imports resolve correctly
        Validates: Requirements 1.4
        
        For any import statement in any Python file, the imported module 
        should exist and be accessible.
        """
        auditor = CodeAuditor()
        import_issues = auditor.audit_imports()
        
        # Filter out known optional dependencies
        optional_deps = ['playwright', 'selenium', 'webdriver_manager']
        critical_issues = [
            issue for issue in import_issues 
            if not any(dep in issue for dep in optional_deps)
        ]
        
        # Property: No critical import issues should exist
        assert len(critical_issues) == 0, f"Found critical import issues: {critical_issues}"
    
    @given(st.sampled_from([
        'src/scraper.py',
        'src/filters.py',
        'src/storage.py',
        'src/ai_gemini.py',
        'src/config.py'
    ]))
    def test_property_critical_files_exist(self, filename):
        """
        Property: All critical system files exist and are readable
        
        For any critical file in the system, the file should exist 
        and be readable.
        """
        file_path = Path(filename)
        assert file_path.exists(), f"Critical file missing: {filename}"
        
        # Should be readable
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 0, f"File is empty: {filename}"
    
    def test_audit_report_generation(self):
        """Test that audit report is generated correctly"""
        auditor = CodeAuditor()
        results = auditor.run_full_audit()
        
        # Verify report structure
        assert 'timestamp' in results
        assert 'syntax_errors' in results
        assert 'import_issues' in results
        assert 'error_handling_gaps' in results
        assert 'duplicate_code' in results
        assert 'integration_issues' in results
        assert 'recommendations' in results
        
        # Verify recommendations are generated
        assert len(results['recommendations']) > 0


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
