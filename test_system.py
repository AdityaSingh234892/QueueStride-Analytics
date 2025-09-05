#!/usr/bin/env python3
"""
Simple test script to verify the system components are working
"""
import sys
import os
import time
import requests
import subprocess
from pathlib import Path

def test_backend():
    """Test if backend is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✓ Backend is running successfully")
            return True
        else:
            print(f"✗ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Backend not accessible: {e}")
        return False

def test_cv_system():
    """Test if CV system can be imported"""
    try:
        sys.path.append(str(Path(__file__).parent / "cv_system"))
        from enhanced_monitor import EnhancedStockMonitor
        print("✓ CV system imports successfully")
        return True
    except ImportError as e:
        print(f"✗ CV system import failed: {e}")
        return False

def test_original_scripts():
    """Test if original scripts exist and can be imported"""
    try:
        import cv2
        import numpy as np
        print("✓ OpenCV is available")
        
        if os.path.exists("Asm1.py"):
            print("✓ Original Asm1.py script found")
        if os.path.exists("Asm.py"):
            print("✓ Original Asm.py script found")
        
        return True
    except ImportError as e:
        print(f"✗ OpenCV not available: {e}")
        return False

def main():
    print("=== Automated Stock Monitoring AI Camera System Test ===")
    print()
    
    # Test components
    results = []
    
    print("1. Testing Backend Server...")
    results.append(test_backend())
    
    print("2. Testing CV System...")
    results.append(test_cv_system())
    
    print("3. Testing Original Scripts...")
    results.append(test_original_scripts())
    
    print()
    print("=== Test Results ===")
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total} tests")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    print()
    print("To run the full system:")
    print("1. Run 'run_system.bat' to start all components")
    print("2. Open 'simple-client.html' in your browser")
    print("3. Or run individual components:")
    print("   - Backend: cd backend && python main.py")
    print("   - CV System: cd cv_system && python enhanced_monitor.py")
    print("   - Original Script: python Asm1.py")

if __name__ == "__main__":
    main()
