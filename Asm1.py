import cv2
import numpy as np
import json
import datetime
from collections import deque
import os
import threading
import time

class AutomatedStockMonitor:
    def __init__(self, camera_id=0, config_file='shelf_config.json'):
        self.cap = cv2.VideoCapture(camera_id)
        self.config_file = config_file
        self.shelf_regions = []
        self.empty_threshold = 0.15  # Threshold for considering shelf empty
        self.alert_history = deque(maxlen=100)
        self.setup_mode = False
        self.monitoring = False
        
        # Load configuration if exists
        self.load_config()
        
        # Initialize background subtractor
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=16, detectShadows=True
        )
        
        # Alert system
        self.alert_cooldown = {}  # Prevent spam alerts
        self.alert_duration = 300  # 5 minutes cooldown
        
    def load_config(self):
        """Load shelf configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.shelf_regions = data.get('shelf_regions', [])
                    self.empty_threshold = data.get('empty_threshold', 0.15)
                print(f"Loaded {len(self.shelf_regions)} shelf regions from config")
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save shelf configuration to file"""
        try:
            config = {
                'shelf_regions': self.shelf_regions,
                'empty_threshold': self.empty_threshold,
                'last_updated': datetime.datetime.now().isoformat()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print("Configuration saved successfully")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def detect_shelves_automatically(self, frame):
        """Automatically detect shelf regions using edge detection and contours"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        potential_shelves = []
        
        for contour in contours:
            # Calculate contour area and bounding rectangle
            area = cv2.contourArea(contour)
            if area < 5000:  # Filter small contours
                continue
                
            x, y, w, h = cv2.boundingRect(contour)
            
            # Filter based on aspect ratio (shelves are typically wider than tall)
            aspect_ratio = w / h
            if aspect_ratio > 1.5 and w > 100 and h > 50:
                potential_shelves.append({
                    'id': len(potential_shelves),
                    'name': f'Auto_Shelf_{len(potential_shelves)}',
                    'region': [x, y, x + w, y + h],
                    'area': area,
                    'aspect_ratio': aspect_ratio
                })
        
        return potential_shelves
    
    def analyze_shelf_occupancy(self, frame, shelf_region):
        """Analyze if a shelf is empty or stocked"""
        x1, y1, x2, y2 = shelf_region
        shelf_roi = frame[y1:y2, x1:x2]
        
        if shelf_roi.size == 0:
            return 0.0, shelf_roi
        
        # Convert to different color spaces for analysis
        gray_roi = cv2.cvtColor(shelf_roi, cv2.COLOR_BGR2GRAY)
        hsv_roi = cv2.cvtColor(shelf_roi, cv2.COLOR_BGR2HSV)
        
        # Method 1: Edge density analysis
        edges = cv2.Canny(gray_roi, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Method 2: Color variance analysis
        color_variance = np.var(gray_roi)
        
        # Method 3: Histogram analysis
        hist = cv2.calcHist([gray_roi], [0], None, [256], [0, 256])
        hist_variance = np.var(hist)
        
        # Method 4: Background subtraction
        fg_mask = self.bg_subtractor.apply(shelf_roi)
        foreground_ratio = np.sum(fg_mask > 0) / (fg_mask.shape[0] * fg_mask.shape[1])
        
        # Combine metrics to determine occupancy
        occupancy_score = (
            edge_density * 0.3 +
            min(color_variance / 1000, 1.0) * 0.3 +
            min(hist_variance / 1000000, 1.0) * 0.2 +
            foreground_ratio * 0.2
        )
        
        return occupancy_score, shelf_roi
    
    def send_alert(self, shelf_info, occupancy_score):
        """Send alert for empty shelf"""
        current_time = datetime.datetime.now()
        shelf_id = shelf_info['id']
        
        # Check cooldown
        if shelf_id in self.alert_cooldown:
            time_diff = (current_time - self.alert_cooldown[shelf_id]).seconds
            if time_diff < self.alert_duration:
                return
        
        # Create alert
        alert = {
            'timestamp': current_time.isoformat(),
            'shelf_id': shelf_id,
            'shelf_name': shelf_info['name'],
            'occupancy_score': occupancy_score,
            'message': f"ALERT: {shelf_info['name']} is empty and needs refilling!",
            'priority': 'HIGH' if occupancy_score < 0.05 else 'MEDIUM'
        }
        
        # Add to history
        self.alert_history.append(alert)
        
        # Update cooldown
        self.alert_cooldown[shelf_id] = current_time
        
        # Print alert (in production, this could be sent to a server/database)
        print(f"\n🚨 {alert['message']}")
        print(f"   Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Occupancy Score: {occupancy_score:.3f}")
        print(f"   Priority: {alert['priority']}")
        
        # Save alert to file
        self.save_alert_to_file(alert)
    
    def save_alert_to_file(self, alert):
        """Save alert to file for logging"""
        try:
            alerts_file = 'alerts.json'
            alerts = []
            
            if os.path.exists(alerts_file):
                with open(alerts_file, 'r') as f:
                    alerts = json.load(f)
            
            alerts.append(alert)
            
            # Keep only last 1000 alerts
            if len(alerts) > 1000:
                alerts = alerts[-1000:]
            
            with open(alerts_file, 'w') as f:
                json.dump(alerts, f, indent=2)
        except Exception as e:
            print(f"Error saving alert: {e}")
    
    def draw_interface(self, frame):
        """Draw monitoring interface on frame"""
        height, width = frame.shape[:2]
        
        # Draw header
        cv2.rectangle(frame, (0, 0), (width, 60), (0, 0, 0), -1)
        cv2.putText(frame, "Automated Stock Monitoring System", (10, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Draw status
        status_text = "SETUP MODE" if self.setup_mode else "MONITORING" if self.monitoring else "STANDBY"
        status_color = (0, 255, 255) if self.setup_mode else (0, 255, 0) if self.monitoring else (0, 0, 255)
        cv2.putText(frame, status_text, (10, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        # Draw shelf count
        cv2.putText(frame, f"Shelves: {len(self.shelf_regions)}", (width - 150, 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw recent alerts count
        recent_alerts = len([a for a in self.alert_history 
                           if (datetime.datetime.now() - datetime.datetime.fromisoformat(a['timestamp'])).seconds < 3600])
        cv2.putText(frame, f"Alerts (1h): {recent_alerts}", (width - 150, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return frame
    
    def draw_shelf_regions(self, frame):
        """Draw shelf regions and their status"""
        for i, shelf in enumerate(self.shelf_regions):
            x1, y1, x2, y2 = shelf['region']
            
            # Analyze occupancy
            occupancy_score, shelf_roi = self.analyze_shelf_occupancy(frame, shelf['region'])
            
            # Determine color based on occupancy
            if occupancy_score < self.empty_threshold:
                color = (0, 0, 255)  # Red for empty
                status = "EMPTY"
                if self.monitoring:
                    self.send_alert(shelf, occupancy_score)
            elif occupancy_score < 0.3:
                color = (0, 165, 255)  # Orange for low stock
                status = "LOW"
            else:
                color = (0, 255, 0)  # Green for stocked
                status = "STOCKED"
            
            # Draw rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw shelf info
            label = f"{shelf['name']} ({status})"
            cv2.putText(frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Draw occupancy score
            score_text = f"{occupancy_score:.3f}"
            cv2.putText(frame, score_text, (x1, y2 + 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        return frame
    
    def setup_shelves_interactive(self):
        """Interactive setup mode for defining shelf regions"""
        print("\n=== SHELF SETUP MODE ===")
        print("Instructions:")
        print("- Press 'a' to auto-detect shelves")
        print("- Click and drag to manually define shelf regions")
        print("- Press 's' to save configuration")
        print("- Press 'c' to clear all regions")
        print("- Press 'q' to quit setup")
        
        self.setup_mode = True
        drawing = False
        start_point = None
        
        def mouse_callback(event, x, y, flags, param):
            nonlocal drawing, start_point
            
            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                start_point = (x, y)
            
            elif event == cv2.EVENT_LBUTTONUP:
                if drawing and start_point:
                    # Add new shelf region
                    x1, y1 = start_point
                    x2, y2 = x, y
                    
                    # Ensure valid rectangle
                    if abs(x2 - x1) > 30 and abs(y2 - y1) > 30:
                        shelf_region = {
                            'id': len(self.shelf_regions),
                            'name': f'Shelf_{len(self.shelf_regions) + 1}',
                            'region': [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
                        }
                        self.shelf_regions.append(shelf_region)
                        print(f"Added {shelf_region['name']} at region {shelf_region['region']}")
                
                drawing = False
                start_point = None
        
        cv2.namedWindow('Setup')
        cv2.setMouseCallback('Setup', mouse_callback)
        
        while self.setup_mode:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = self.draw_interface(frame)
            frame = self.draw_shelf_regions(frame)
            
            # Draw current selection
            if drawing and start_point:
                cv2.rectangle(frame, start_point, (0, 0), (255, 255, 0), 2)
            
            cv2.imshow('Setup', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.setup_mode = False
            elif key == ord('a'):
                # Auto-detect shelves
                detected_shelves = self.detect_shelves_automatically(frame)
                print(f"Auto-detected {len(detected_shelves)} potential shelves")
                
                # Add detected shelves to regions
                for shelf in detected_shelves:
                    shelf['id'] = len(self.shelf_regions)
                    self.shelf_regions.append(shelf)
                
            elif key == ord('s'):
                # Save configuration
                self.save_config()
                
            elif key == ord('c'):
                # Clear all regions
                self.shelf_regions = []
                print("Cleared all shelf regions")
        
        cv2.destroyWindow('Setup')
    
    def monitor_shelves(self):
        """Main monitoring loop"""
        print("\n=== MONITORING MODE ===")
        print("Press 'q' to quit monitoring")
        print("Press 'p' to pause/resume")
        print("Press 'r' to reset background model")
        
        self.monitoring = True
        paused = False
        
        while self.monitoring:
            if not paused:
                ret, frame = self.cap.read()
                if not ret:
                    break
                
                frame = self.draw_interface(frame)
                frame = self.draw_shelf_regions(frame)
                
                cv2.imshow('Monitoring', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.monitoring = False
            elif key == ord('p'):
                paused = not paused
                status = "PAUSED" if paused else "RESUMED"
                print(f"Monitoring {status}")
            elif key == ord('r'):
                # Reset background subtractor
                self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
                    history=500, varThreshold=16, detectShadows=True
                )
                print("Background model reset")
        
        cv2.destroyWindow('Monitoring')
    
    def run(self):
        """Main application loop"""
        print("=== AUTOMATED STOCK MONITORING AI CAMERA ===")
        print("1. Setup shelves")
        print("2. Start monitoring")
        print("3. View alerts")
        print("4. Quit")
        
        while True:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.setup_shelves_interactive()
            elif choice == '2':
                if len(self.shelf_regions) == 0:
                    print("No shelves configured. Please setup shelves first.")
                else:
                    self.monitor_shelves()
            elif choice == '3':
                self.view_alerts()
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")
        
        self.cleanup()
    
    def view_alerts(self):
        """View recent alerts"""
        print("\n=== RECENT ALERTS ===")
        if not self.alert_history:
            print("No alerts recorded.")
            return
        
        # Show last 10 alerts
        recent_alerts = list(self.alert_history)[-10:]
        for alert in reversed(recent_alerts):
            timestamp = datetime.datetime.fromisoformat(alert['timestamp'])
            print(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {alert['message']}")
            print(f"  Priority: {alert['priority']}, Score: {alert['occupancy_score']:.3f}")
    
    def cleanup(self):
        """Cleanup resources"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("System shutdown complete.")

# Example usage
if __name__ == "__main__":
    # Initialize the monitoring system
    monitor = AutomatedStockMonitor(camera_id=0)
    
    # Run the application
    monitor.run()