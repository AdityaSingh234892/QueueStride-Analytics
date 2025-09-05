#!/usr/bin/env python3
"""
Complete System Runner - Starts all components of the AI Camera System
"""
import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path
import threading
import requests

class SystemRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.processes = []
        
    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🚀 Starting Backend Server...")
        backend_path = self.project_root / "backend"
        os.chdir(backend_path)
        
        # Start backend in a new process
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        self.processes.append(("Backend", process))
        print("✅ Backend server starting on http://localhost:8000")
        return process
    
    def start_cv_system(self):
        """Start the enhanced CV monitoring system"""
        print("📹 Starting CV System...")
        cv_path = self.project_root / "cv_system"
        os.chdir(cv_path)
        
        # Start CV system in a new process
        process = subprocess.Popen([
            sys.executable, "enhanced_monitor.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        self.processes.append(("CV System", process))
        print("✅ CV monitoring system started")
        return process
    
    def run_original_script(self):
        """Run the original OpenCV script"""
        print("🔍 Running Original OpenCV Script...")
        os.chdir(self.project_root)
        
        # Start original script in a new process
        process = subprocess.Popen([
            sys.executable, "Asm.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        self.processes.append(("Original Script", process))
        print("✅ Original OpenCV script started")
        return process
    
    def open_web_interfaces(self):
        """Open web interfaces in browser"""
        print("🌐 Opening Web Interfaces...")
        
        # Open dashboard
        dashboard_path = self.project_root / "dashboard.html"
        webbrowser.open(f"file://{dashboard_path.absolute()}")
        
        # Wait a bit then open API docs
        time.sleep(2)
        webbrowser.open("http://localhost:8000/docs")
        
        # Open simple client
        time.sleep(1)
        client_path = self.project_root / "simple-client.html"
        webbrowser.open(f"file://{client_path.absolute()}")
        
        print("✅ Web interfaces opened")
    
    def wait_for_backend(self, timeout=30):
        """Wait for backend to be ready"""
        print("⏳ Waiting for backend to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ Backend is ready!")
                    return True
            except:
                pass
            time.sleep(1)
        
        print("⚠️  Backend might not be ready yet")
        return False
    
    def monitor_processes(self):
        """Monitor running processes"""
        print("\n📊 System Status Monitor")
        print("=" * 50)
        
        while True:
            print(f"\n[{time.strftime('%H:%M:%S')}] Process Status:")
            
            for name, process in self.processes:
                if process.poll() is None:
                    print(f"  ✅ {name}: Running")
                else:
                    print(f"  ❌ {name}: Stopped (Exit code: {process.returncode})")
            
            # Check backend health
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("  🌐 Backend API: Healthy")
                else:
                    print("  ⚠️  Backend API: Issues")
            except:
                print("  ❌ Backend API: Not responding")
            
            print("\nPress Ctrl+C to stop all processes...")
            time.sleep(10)
    
    def cleanup(self):
        """Stop all processes"""
        print("\n🛑 Stopping all processes...")
        for name, process in self.processes:
            if process.poll() is None:
                process.terminate()
                print(f"  Stopped {name}")
        
        print("✅ Cleanup complete")
    
    def run_complete_system(self):
        """Run the complete system"""
        print("🚀 AUTOMATED STOCK MONITORING AI CAMERA SYSTEM")
        print("=" * 60)
        print("Starting all components...")
        print()
        
        try:
            # 1. Start backend
            self.start_backend()
            time.sleep(3)
            
            # 2. Wait for backend to be ready
            self.wait_for_backend()
            
            # 3. Start CV system
            self.start_cv_system()
            time.sleep(2)
            
            # 4. Run original script
            self.run_original_script()
            time.sleep(2)
            
            # 5. Open web interfaces
            self.open_web_interfaces()
            time.sleep(2)
            
            print("\n🎉 SYSTEM FULLY OPERATIONAL!")
            print("=" * 60)
            print("✅ Backend Server: http://localhost:8000")
            print("✅ API Documentation: http://localhost:8000/docs")
            print("✅ Dashboard: dashboard.html")
            print("✅ CV System: Running with camera detection")
            print("✅ Original Script: Monitoring shelves")
            print()
            print("🎯 All components are now running!")
            print("   Check the opened browser tabs for interfaces")
            print("   CV windows should appear for camera monitoring")
            print()
            
            # 6. Monitor the system
            self.monitor_processes()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Shutdown requested by user")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        finally:
            self.cleanup()

def main():
    """Main function"""
    print("Choose how to run the system:")
    print("1. Complete System (All components)")
    print("2. Backend Only")
    print("3. CV System Only") 
    print("4. Original Script Only")
    print("5. Web Interfaces Only")
    
    choice = input("\nEnter choice (1-5) or press Enter for complete system: ").strip()
    
    runner = SystemRunner()
    
    if choice == "2":
        runner.start_backend()
        runner.wait_for_backend()
        input("Press Enter to stop...")
        runner.cleanup()
    elif choice == "3":
        runner.start_cv_system()
        input("Press Enter to stop...")
        runner.cleanup()
    elif choice == "4":
        runner.run_original_script()
        input("Press Enter to stop...")
        runner.cleanup()
    elif choice == "5":
        runner.open_web_interfaces()
        input("Press Enter to exit...")
    else:
        # Default: run complete system
        runner.run_complete_system()

if __name__ == "__main__":
    main()
