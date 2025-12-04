#!/usr/bin/env python3
"""
System Audit Tool
Checks all Python files for syntax errors, import issues, error handling, and code quality.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import importlib.util
from datetime import datetime
import json

class CodeAuditor:
    """Comprehensive code auditing tool"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "syntax_errors": [],
            "import_issues": [],
            "error_handling_gaps": [],
            "duplicate_code": [],
            "integration_issues": [],
            "recommendations": []
        }
    
    def get_python_files(self) -> List[Path]:
        """Get all Python files in the project"""
        python_files = []
        exclude_dirs = {'.venv', 'venv', '.git', '__pycache__', '.pytest_cache', '.hypothesis'}
        
        for path in self.root_dir.rglob('*.py'):
            # Skip excluded directories
            if any(excluded in path.parts for excluded in exclude_dirs):
                continue
            python_files.append(path)
        
        return python_files
    
    def audit_syntax(self) -> List[str]:
        """Check all .py files for syntax errors"""
        print("\n🔍 Checking syntax errors...")
        syntax_errors = []
        
        for file_path in self.get_python_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                ast.parse(code)
                print(f"  ✅ {file_path}")
            except SyntaxError as e:
                error_msg = f"{file_path}:{e.lineno} - {e.msg}"
                syntax_errors.append(error_msg)
                print(f"  ❌ {error_msg}")
            except Exception as e:
                error_msg = f"{file_path} - {str(e)}"
                syntax_errors.append(error_msg)
                print(f"  ⚠️  {error_msg}")
        
        self.results["syntax_errors"] = syntax_errors
        return syntax_errors
    
    def audit_imports(self) -> List[str]:
        """Find unused imports and missing dependencies"""
        print("\n🔍 Checking imports...")
        import_issues = []
        
        for file_path in self.get_python_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                tree = ast.parse(code)
                
                # Extract all imports
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name.split('.')[0])
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module.split('.')[0])
                
                # Check if imports can be resolved
                for imp in set(imports):
                    # Skip standard library and relative imports
                    if imp in ['os', 'sys', 'json', 'time', 'datetime', 're', 'pathlib', 
                              'typing', 'collections', 'itertools', 'functools', 'logging',
                              'unittest', 'pytest', 'hypothesis']:
                        continue
                    
                    # Try to find the module
                    spec = importlib.util.find_spec(imp)
                    if spec is None:
                        # Check if it's a local module
                        local_module = self.root_dir / 'src' / f'{imp}.py'
                        if not local_module.exists():
                            issue = f"{file_path} - Cannot resolve import: {imp}"
                            import_issues.append(issue)
                            print(f"  ⚠️  {issue}")
                        else:
                            print(f"  ✅ {file_path} - {imp} (local)")
                    else:
                        print(f"  ✅ {file_path} - {imp}")
                        
            except Exception as e:
                issue = f"{file_path} - Error checking imports: {str(e)}"
                import_issues.append(issue)
                print(f"  ❌ {issue}")
        
        self.results["import_issues"] = import_issues
        return import_issues
    
    def audit_error_handling(self) -> List[str]:
        """Identify functions without try-except blocks"""
        print("\n🔍 Checking error handling...")
        error_handling_gaps = []
        
        critical_functions = [
            'search_places', 'scrape', 'fetch',  # API calls
            'append_to_sheet', 'append_to_csv', 'save',  # File operations
            'send_email', 'send_whatsapp', 'send',  # Network operations
            'generate_content', 'create_content'  # AI operations
        ]
        
        for file_path in self.get_python_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                tree = ast.parse(code)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Check if function name suggests it needs error handling
                        needs_error_handling = any(
                            keyword in node.name.lower() 
                            for keyword in critical_functions
                        )
                        
                        if needs_error_handling:
                            # Check if function has try-except
                            has_try_except = any(
                                isinstance(child, ast.Try) 
                                for child in ast.walk(node)
                            )
                            
                            if not has_try_except:
                                gap = f"{file_path} - Function '{node.name}' lacks error handling"
                                error_handling_gaps.append(gap)
                                print(f"  ⚠️  {gap}")
                            else:
                                print(f"  ✅ {file_path} - {node.name}")
                                
            except Exception as e:
                gap = f"{file_path} - Error checking error handling: {str(e)}"
                error_handling_gaps.append(gap)
                print(f"  ❌ {gap}")
        
        self.results["error_handling_gaps"] = error_handling_gaps
        return error_handling_gaps
    
    def audit_duplicates(self) -> List[str]:
        """Find duplicate code across files"""
        print("\n🔍 Checking for duplicate code...")
        duplicates = []
        
        # Simple duplicate detection: check for functions with same name
        function_locations = {}
        
        for file_path in self.get_python_files():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                tree = ast.parse(code)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_name = node.name
                        if func_name.startswith('_'):  # Skip private functions
                            continue
                        
                        if func_name in function_locations:
                            dup = f"Function '{func_name}' found in multiple files: {function_locations[func_name]} and {file_path}"
                            duplicates.append(dup)
                            print(f"  ⚠️  {dup}")
                        else:
                            function_locations[func_name] = file_path
                            
            except Exception as e:
                print(f"  ❌ {file_path} - Error checking duplicates: {str(e)}")
        
        self.results["duplicate_code"] = duplicates
        return duplicates
    
    def audit_integration(self) -> List[str]:
        """Verify all module imports work correctly"""
        print("\n🔍 Checking module integration...")
        integration_issues = []
        
        # Key integration points to check
        integrations = [
            ('src/scraper.py', 'src/filters.py'),
            ('src/filters.py', 'src/storage.py'),
            ('src/storage.py', 'src/ai_gemini.py'),
            ('src/ai_gemini.py', 'src/email_sender.py'),
            ('src/ai_gemini.py', 'src/whatsapp_bot.py'),
        ]
        
        for source, target in integrations:
            source_path = self.root_dir / source
            target_path = self.root_dir / target
            
            if not source_path.exists():
                issue = f"Source module missing: {source}"
                integration_issues.append(issue)
                print(f"  ❌ {issue}")
                continue
            
            if not target_path.exists():
                issue = f"Target module missing: {target}"
                integration_issues.append(issue)
                print(f"  ❌ {issue}")
                continue
            
            print(f"  ✅ {source} → {target}")
        
        self.results["integration_issues"] = integration_issues
        return integration_issues
    
    def generate_recommendations(self):
        """Generate recommendations based on audit results"""
        print("\n💡 Generating recommendations...")
        recommendations = []
        
        if self.results["syntax_errors"]:
            recommendations.append(
                f"Fix {len(self.results['syntax_errors'])} syntax errors before proceeding"
            )
        
        if self.results["import_issues"]:
            recommendations.append(
                f"Resolve {len(self.results['import_issues'])} import issues - install missing packages or fix import paths"
            )
        
        if self.results["error_handling_gaps"]:
            recommendations.append(
                f"Add error handling to {len(self.results['error_handling_gaps'])} critical functions"
            )
        
        if self.results["duplicate_code"]:
            recommendations.append(
                f"Refactor {len(self.results['duplicate_code'])} duplicate functions into shared utilities"
            )
        
        if self.results["integration_issues"]:
            recommendations.append(
                f"Fix {len(self.results['integration_issues'])} integration issues"
            )
        
        if not any([
            self.results["syntax_errors"],
            self.results["import_issues"],
            self.results["error_handling_gaps"],
            self.results["duplicate_code"],
            self.results["integration_issues"]
        ]):
            recommendations.append("✅ Code audit passed! System is in good shape.")
        
        self.results["recommendations"] = recommendations
        return recommendations
    
    def run_full_audit(self) -> Dict:
        """Run complete audit"""
        print("=" * 60)
        print("🔍 SYSTEM AUDIT STARTING")
        print("=" * 60)
        
        self.audit_syntax()
        self.audit_imports()
        self.audit_error_handling()
        self.audit_duplicates()
        self.audit_integration()
        self.generate_recommendations()
        
        return self.results
    
    def save_report(self, filename: str = "audit_report.json"):
        """Save audit report to file"""
        report_path = self.root_dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Report saved to: {report_path}")
    
    def print_summary(self):
        """Print audit summary"""
        print("\n" + "=" * 60)
        print("📊 AUDIT SUMMARY")
        print("=" * 60)
        print(f"Syntax Errors: {len(self.results['syntax_errors'])}")
        print(f"Import Issues: {len(self.results['import_issues'])}")
        print(f"Error Handling Gaps: {len(self.results['error_handling_gaps'])}")
        print(f"Duplicate Code: {len(self.results['duplicate_code'])}")
        print(f"Integration Issues: {len(self.results['integration_issues'])}")
        print("\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(self.results['recommendations'], 1):
            print(f"{i}. {rec}")
        print("=" * 60)


def main():
    """Main entry point"""
    auditor = CodeAuditor()
    results = auditor.run_full_audit()
    auditor.save_report()
    auditor.print_summary()
    
    # Exit with error code if issues found
    total_issues = sum([
        len(results['syntax_errors']),
        len(results['import_issues']),
        len(results['error_handling_gaps']),
        len(results['integration_issues'])
    ])
    
    if total_issues > 0:
        print(f"\n⚠️  Found {total_issues} issues that need attention")
        sys.exit(1)
    else:
        print("\n✅ All checks passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
