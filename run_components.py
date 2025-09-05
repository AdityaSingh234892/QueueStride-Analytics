#!/usr/bin/env python3
"""
Manual System Runner - Starts each component individually
"""
import subprocess
import sys
import os
import webbrowser
from pathlib import Path
import time

def run_backend():
    """Start the backend server"""
    print("Starting Backend Server...")
    backend_path = Path(__file__).parent / "backend"
    os.chdir(backend_path)
    subprocess.Popen([sys.executable, "main.py"])
    print("Backend server started on http://localhost:8000")
    return True

def run_cv_system():
    """Start the CV monitoring system"""
    print("Starting CV System...")
    cv_path = Path(__file__).parent / "cv_system"
    os.chdir(cv_path)
    subprocess.Popen([sys.executable, "enhanced_monitor.py"])
    print("CV system started")
    return True

def run_original_script():
    """Run the original OpenCV script"""
    print("Running Original OpenCV Script...")
    project_path = Path(__file__).parent
    os.chdir(project_path)
    subprocess.Popen([sys.executable, "Asm1.py"])
    print("Original script started")
    return True

def open_client():
    """Open the simple HTML client"""
    print("Opening Simple HTML Client...")
    client_path = Path(__file__).parent / "simple-client.html"
    webbrowser.open(f"file://{client_path.absolute()}")
    print("HTML client opened in browser")
    return True

def main():
    print("=== Automated Stock Monitoring AI Camera System ===")
    print()
    
    while True:
        print("Choose an option:")
        print("1. Start Backend Server")
        print("2. Start CV System")
        print("3. Run Original Script (Asm1.py)")
        print("4. Open Simple HTML Client")
        print("5. Start All Components")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            run_backend()
        elif choice == "2":
            run_cv_system()
        elif choice == "3":
            run_original_script()
        elif choice == "4":
            open_client()
        elif choice == "5":
            print("Starting all components...")
            run_backend()
            time.sleep(2)
            run_cv_system()
            time.sleep(1)
            open_client()
            print("All components started!")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        print()

if __name__ == "__main__":
    main()
