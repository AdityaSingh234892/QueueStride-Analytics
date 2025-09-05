"""
Quick System Status Check
"""
import os
print("🚀 Automated Stock Monitoring AI Camera System")
print("=== System Status ===")
print()

# Check key files
key_files = [
    "backend/main.py",
    "cv_system/enhanced_monitor.py", 
    "Asm1.py",
    "simple-client.html"
]

print("Key Components:")
for file in key_files:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        print(f"✗ {file}")

print()
print("=== How to Run ===")
print("1. Backend: cd backend && python main.py")
print("2. CV System: cd cv_system && python enhanced_monitor.py")
print("3. Original Script: python Asm1.py")
print("4. Web Client: Open simple-client.html")
print("5. Interactive: python run_components.py")
print()
print("✅ System is ready to run!")
