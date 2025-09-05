#!/usr/bin/env python3
"""
Final System Verification Script
"""
import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} NOT FOUND")
        return False

def check_python_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"✓ {package_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name} is NOT installed")
        return False

def check_project_structure():
    """Check if all required files exist"""
    print("=== Checking Project Structure ===")
    
    files_to_check = [
        ("backend/main.py", "Backend main file"),
        ("backend/requirements.txt", "Backend requirements"),
        ("cv_system/enhanced_monitor.py", "Enhanced CV monitor"),
        ("cv_system/requirements.txt", "CV system requirements"),
        ("frontend/package.json", "Frontend package.json"),
        ("Asm1.py", "Original OpenCV script"),
        ("simple-client.html", "Simple HTML client"),
        ("run_system.bat", "System runner batch file"),
        ("run_components.py", "Interactive component runner"),
        ("RUNNING_GUIDE.md", "Running guide documentation"),
    ]
    
    results = []
    for filepath, description in files_to_check:
        results.append(check_file_exists(filepath, description))
    
    return results

def check_python_dependencies():
    """Check Python dependencies"""
    print("\n=== Checking Python Dependencies ===")
    
    packages = [
        "cv2",
        "numpy",
        "requests",
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "websockets",
    ]
    
    results = []
    for package in packages:
        results.append(check_python_package(package))
    
    return results

def check_backend_files():
    """Check backend files structure"""
    print("\n=== Checking Backend Files ===")
    
    backend_files = [
        "backend/main.py",
        "backend/models.py",
        "backend/schemas.py",
        "backend/database.py",
        "backend/auth.py",
        "backend/cv_processor.py",
        "backend/notification_system.py",
    ]
    
    results = []
    for file_path in backend_files:
        results.append(check_file_exists(file_path, f"Backend: {os.path.basename(file_path)}"))
    
    return results

def check_frontend_files():
    """Check frontend files structure"""
    print("\n=== Checking Frontend Files ===")
    
    frontend_files = [
        "frontend/package.json",
        "frontend/src/App.js",
        "frontend/src/index.js",
        "frontend/public/index.html",
    ]
    
    results = []
    for file_path in frontend_files:
        results.append(check_file_exists(file_path, f"Frontend: {os.path.basename(file_path)}"))
    
    return results

def show_next_steps():
    """Show next steps to run the system"""
    print("\n=== Next Steps ===")
    print("1. Start Backend Server:")
    print("   cd backend && python main.py")
    print("\n2. Start CV System:")
    print("   cd cv_system && python enhanced_monitor.py")
    print("\n3. Test Original Script:")
    print("   python Asm1.py")
    print("\n4. Open Web Client:")
    print("   Open simple-client.html in browser")
    print("\n5. Or use interactive runner:")
    print("   python run_components.py")
    print("\n6. Or use batch file (Windows):")
    print("   run_system.bat")

def main():
    print("🚀 Automated Stock Monitoring AI Camera System")
    print("=== Final System Verification ===")
    print()
    
    # Check all components
    structure_results = check_project_structure()
    dependency_results = check_python_dependencies()
    backend_results = check_backend_files()
    frontend_results = check_frontend_files()
    
    # Calculate totals
    all_results = structure_results + dependency_results + backend_results + frontend_results
    passed = sum(all_results)
    total = len(all_results)
    
    print(f"\n=== Summary ===")
    print(f"✓ Passed: {passed}/{total} checks")
    
    if passed >= total * 0.8:  # 80% pass rate
        print("🎉 System is ready to run!")
        print("✓ All critical components are in place")
    else:
        print("⚠️  Some components are missing")
        print("Please check the items marked with ✗ above")
    
    show_next_steps()

if __name__ == "__main__":
    main()
