#!/usr/bin/env python3
"""
Complete System Launcher - Starts all components of the AI Camera System
"""
import subprocess
import sys
import os
import time
import webbrowser
import threading
import requests
from pathlib import Path

class SystemLauncher:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.backend_process = None
        self.cv_process = None
        self.original_process = None
        self.running = False
        
    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🔧 Starting Backend Server...")
        backend_dir = self.project_dir / "backend"
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=backend_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            print("   ✅ Backend server started")
            return True
        except Exception as e:
            print(f"   ❌ Backend failed to start: {e}")
            return False
    
    def start_cv_system(self):
        """Start the CV monitoring system"""
        print("🎥 Starting CV Monitoring System...")
        cv_dir = self.project_dir / "cv_system"
        try:
            self.cv_process = subprocess.Popen(
                [sys.executable, "enhanced_monitor.py"],
                cwd=cv_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            print("   ✅ CV system started")
            return True
        except Exception as e:
            print(f"   ❌ CV system failed to start: {e}")
            return False
    
    def start_original_script(self):
        """Start the original OpenCV script"""
        print("📹 Starting Original OpenCV Script...")
        try:
            self.original_process = subprocess.Popen(
                [sys.executable, "Asm1.py"],
                cwd=self.project_dir,
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            print("   ✅ Original script started")
            return True
        except Exception as e:
            print(f"   ❌ Original script failed to start: {e}")
            return False
    
    def wait_for_backend(self, timeout=30):
        """Wait for backend to be ready"""
        print("⏱️ Waiting for backend to initialize...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("   ✅ Backend is healthy and ready")
                    return True
            except:
                time.sleep(1)
        print("   ⚠️ Backend may still be starting...")
        return False
    
    def open_web_interfaces(self):
        """Open web interfaces in browser"""
        print("🌐 Opening Web Interfaces...")
        try:
            # Open dashboard
            dashboard_path = self.project_dir / "dashboard.html"
            webbrowser.open(f"file://{dashboard_path.absolute()}")
            
            # Wait a moment
            time.sleep(2)
            
            # Open API docs
            webbrowser.open("http://localhost:8000/docs")
            
            print("   ✅ Web interfaces opened")
            return True
        except Exception as e:
            print(f"   ❌ Failed to open web interfaces: {e}")
            return False
    
    def monitor_system(self):
        """Monitor system health"""
        print("\n🔍 Monitoring system health...")
        while self.running:
            try:
                # Check backend health
                response = requests.get("http://localhost:8000/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Backend healthy: {data['status']}")
                else:
                    print(f"   ⚠️ Backend returned {response.status_code}")
            except:
                print("   ❌ Backend not responding")
            
            # Check processes
            if self.backend_process and self.backend_process.poll() is not None:
                print("   ⚠️ Backend process terminated")
            
            if self.cv_process and self.cv_process.poll() is not None:
                print("   ⚠️ CV process terminated")
            
            time.sleep(30)  # Check every 30 seconds
    
    def start_complete_system(self):
        """Start the complete system"""
        print("=" * 60)
        print("🚀 AUTOMATED STOCK MONITORING AI CAMERA SYSTEM")
        print("🏪 STARTING COMPLETE PROJECT...")
        print("=" * 60)
        print()
        
        # Start components
        results = []
        
        # 1. Start backend
        results.append(self.start_backend())
        
        # 2. Wait for backend
        if results[-1]:
            time.sleep(3)
            self.wait_for_backend()
        
        # 3. Start CV system
        results.append(self.start_cv_system())
        time.sleep(2)
        
        # 4. Start original script
        results.append(self.start_original_script())
        time.sleep(2)
        
        # 5. Open web interfaces
        results.append(self.open_web_interfaces())
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 SYSTEM STATUS")
        print("=" * 60)
        
        passed = sum(results)
        total = len(results)
        
        print(f"✅ Components started: {passed}/{total}")
        
        if passed >= 3:
            print("🎉 SYSTEM IS RUNNING!")
            print("\n🎯 Access Points:")
            print("   • Dashboard: dashboard.html (opened)")
            print("   • Backend API: http://localhost:8000")
            print("   • API Docs: http://localhost:8000/docs (opened)")
            print("   • Health Check: http://localhost:8000/health")
            
            print("\n🎮 Running Components:")
            print("   • Backend Server (FastAPI) - Port 8000")
            print("   • CV Monitoring System (OpenCV)")
            print("   • Original Script (Asm1.py)")
            print("   • Web Dashboard (HTML)")
            
            print("\n📋 Controls:")
            print("   • Press Ctrl+C to stop monitoring")
            print("   • Close terminal windows to stop components")
            
            # Start monitoring
            self.running = True
            monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
            monitor_thread.start()
            
            print("\n🎊 YOUR AI CAMERA SYSTEM IS NOW LIVE!")
            print("=" * 60)
            
            # Keep the script running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 Stopping system...")
                self.stop_system()
        else:
            print("❌ Some components failed to start")
            print("Please check the error messages above")
    
    def stop_system(self):
        """Stop all system components"""
        print("🛑 Stopping system components...")
        self.running = False
        
        if self.backend_process:
            self.backend_process.terminate()
            print("   ✅ Backend stopped")
        
        if self.cv_process:
            self.cv_process.terminate()
            print("   ✅ CV system stopped")
        
        if self.original_process:
            self.original_process.terminate()
            print("   ✅ Original script stopped")
        
        print("🎯 System shutdown complete")

def main():
    launcher = SystemLauncher()
    launcher.start_complete_system()

if __name__ == "__main__":
    main()
