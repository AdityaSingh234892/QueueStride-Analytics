"""
AUTOMATED STOCK MONITORING AI CAMERA SYSTEM
============================================
Complete Project Status and Runner
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def show_system_status():
    """Show current system status"""
    print("🚀 AUTOMATED STOCK MONITORING AI CAMERA SYSTEM")
    print("=" * 60)
    print()
    
    # Check project files
    project_files = [
        ("Asm.py", "Original OpenCV Script"),
        ("Asm1.py", "Alternative OpenCV Script"),
        ("backend/main.py", "FastAPI Backend Server"),
        ("cv_system/enhanced_monitor.py", "Enhanced CV System"),
        ("dashboard.html", "System Dashboard"),
        ("simple-client.html", "Simple Web Client"),
    ]
    
    print("📋 PROJECT COMPONENTS:")
    for file_path, description in project_files:
        if os.path.exists(file_path):
            print(f"  ✅ {description}: {file_path}")
        else:
            print(f"  ❌ {description}: {file_path} (MISSING)")
    
    print()
    
    # Check Python dependencies
    print("🐍 PYTHON DEPENDENCIES:")
    dependencies = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("requests", "Requests"),
    ]
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"  ✅ {name}: Available")
        except ImportError:
            print(f"  ❌ {name}: NOT INSTALLED")
    
    print()

def run_original_opencv():
    """Run the original OpenCV script"""
    print("🔍 RUNNING ORIGINAL OPENCV SCRIPT")
    print("=" * 40)
    print("Starting Asm.py...")
    print("This will open a video window with shelf monitoring")
    print("Press 'q' in the video window to quit")
    print()
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, "Asm.py"], 
                              capture_output=False, text=True)
        if result.returncode == 0:
            print("✅ Script completed successfully")
        else:
            print("❌ Script ended with error")
    except Exception as e:
        print(f"❌ Error running script: {e}")

def start_backend_server():
    """Start the backend server"""
    print("🚀 STARTING BACKEND SERVER")
    print("=" * 40)
    print("Starting FastAPI server...")
    print("Server will run on: http://localhost:8000")
    print("API docs will be at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        os.chdir("backend")
        subprocess.run([sys.executable, "main.py"])
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
    finally:
        os.chdir("..")

def start_cv_system():
    """Start the enhanced CV system"""
    print("📹 STARTING ENHANCED CV SYSTEM")
    print("=" * 40)
    print("Starting enhanced monitoring...")
    print("This will open camera feed with advanced detection")
    print("Press 'q' to quit, 's' to toggle setup mode")
    print()
    
    try:
        os.chdir("cv_system")
        subprocess.run([sys.executable, "enhanced_monitor.py"])
    except Exception as e:
        print(f"❌ Error starting CV system: {e}")
    finally:
        os.chdir("..")

def open_web_interfaces():
    """Open web interfaces"""
    print("🌐 OPENING WEB INTERFACES")
    print("=" * 40)
    
    # Open dashboard
    dashboard_path = Path("dashboard.html").absolute()
    print(f"Opening dashboard: {dashboard_path}")
    webbrowser.open(f"file://{dashboard_path}")
    
    time.sleep(1)
    
    # Open simple client
    client_path = Path("simple-client.html").absolute()
    print(f"Opening simple client: {client_path}")
    webbrowser.open(f"file://{client_path}")
    
    time.sleep(1)
    
    # Try to open API docs (if backend is running)
    print("Attempting to open API documentation...")
    webbrowser.open("http://localhost:8000/docs")
    
    print("✅ Web interfaces opened in browser")

def run_complete_system():
    """Run the complete system"""
    print("🎉 STARTING COMPLETE SYSTEM")
    print("=" * 40)
    print()
    
    # Open web interfaces first
    print("1. Opening web interfaces...")
    open_web_interfaces()
    
    print("\n2. Starting backend server in new window...")
    subprocess.Popen([
        "cmd", "/c", 
        f"cd /d {os.getcwd()}\\backend && python main.py && pause"
    ], creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    time.sleep(3)
    
    print("3. Starting CV system in new window...")
    subprocess.Popen([
        "cmd", "/c", 
        f"cd /d {os.getcwd()}\\cv_system && python enhanced_monitor.py && pause"
    ], creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    time.sleep(2)
    
    print("4. Starting original script in new window...")
    subprocess.Popen([
        "cmd", "/c", 
        f"cd /d {os.getcwd()} && python Asm.py && pause"
    ], creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    print()
    print("🎉 COMPLETE SYSTEM STARTED!")
    print("=" * 40)
    print("✅ Backend Server: Check new console window")
    print("✅ CV System: Check new console window") 
    print("✅ Original Script: Check new console window")
    print("✅ Web Interfaces: Check browser tabs")
    print()
    print("🎯 Your AI Camera System is now fully operational!")

def main():
    """Main menu"""
    show_system_status()
    
    while True:
        print("🎮 SYSTEM RUNNER MENU")
        print("=" * 40)
        print("1. Run Original OpenCV Script (Asm.py)")
        print("2. Start Backend Server")
        print("3. Start Enhanced CV System")
        print("4. Open Web Interfaces")
        print("5. Run Complete System (ALL)")
        print("6. Show System Status")
        print("7. Exit")
        print()
        
        choice = input("Enter your choice (1-7): ").strip()
        print()
        
        if choice == "1":
            run_original_opencv()
        elif choice == "2":
            start_backend_server()
        elif choice == "3":
            start_cv_system()
        elif choice == "4":
            open_web_interfaces()
        elif choice == "5":
            run_complete_system()
            break  # Exit after starting complete system
        elif choice == "6":
            show_system_status()
        elif choice == "7":
            print("👋 Thank you for using the AI Camera System!")
            break
        else:
            print("❌ Invalid choice. Please try again.")
        
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
