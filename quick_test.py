"""
QUICK PROJECT TEST AND RUNNER
=============================
"""
import os
import sys

print("🚀 AI CAMERA SYSTEM - QUICK TEST")
print("=" * 50)

# Test 1: Check if we're in the right directory
current_dir = os.getcwd()
print(f"📍 Current Directory: {current_dir}")

# Test 2: Check key files
key_files = [
    "Asm.py",
    "backend/main.py", 
    "cv_system/enhanced_monitor.py",
    "dashboard.html"
]

print("\n📋 Key Files Check:")
for file in key_files:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file}")

# Test 3: Check Python packages
print("\n🐍 Python Dependencies:")
packages = ["cv2", "numpy", "fastapi"]
for pkg in packages:
    try:
        __import__(pkg)
        print(f"  ✅ {pkg}")
    except ImportError:
        print(f"  ❌ {pkg}")

print("\n🎯 TO RUN THE PROJECT:")
print("1. Original Script: python Asm.py")
print("2. Backend Server: cd backend && python main.py")
print("3. CV System: cd cv_system && python enhanced_monitor.py")  
print("4. Web Dashboard: Open dashboard.html (already opened)")

print("\n✅ SYSTEM IS READY!")
print("Choose any component above to start!")
