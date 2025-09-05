import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import logging
import asyncio
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class NotificationSystem:
    def __init__(self):
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': '',  # Set via environment variable
            'password': '',  # Set via environment variable
        }
        
    def send_email_alert(self, recipient: str, subject: str, message: str) -> bool:
        """Send email alert"""
        try:
            if not self.email_config['username'] or not self.email_config['password']:
                logger.warning("Email credentials not configured")
                return False
                
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['username']
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(message, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['username'], recipient, text)
            server.quit()
            
            logger.info(f"Email sent to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_push_notification(self, user_id: str, title: str, message: str) -> bool:
        """Send push notification (placeholder for actual implementation)"""
        try:
            # This is a placeholder. In a real implementation, you would use
            # services like Firebase Cloud Messaging (FCM), Apple Push Notification service (APNs),
            # or a service like Pusher or Socket.IO
            
            notification_data = {
                'user_id': user_id,
                'title': title,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Push notification sent to {user_id}: {title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send push notification: {str(e)}")
            return False
    
    def send_sms_alert(self, phone_number: str, message: str) -> bool:
        """Send SMS alert (placeholder for actual implementation)"""
        try:
            # This is a placeholder. In a real implementation, you would use
            # services like Twilio, AWS SNS, or similar SMS providers
            
            logger.info(f"SMS sent to {phone_number}: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            return False
    
    async def send_alert_notifications(self, alert_data: Dict[str, Any], user_preferences: Dict[str, Any]) -> Dict[str, bool]:
        """Send alert notifications based on user preferences"""
        results = {}
        
        try:
            # Prepare notification content
            title = f"Stock Alert: {alert_data['shelf_name']}"
            message = f"{alert_data['message']}\nOccupancy Score: {alert_data['occupancy_score']:.3f}\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Send email if enabled
            if user_preferences.get('email_enabled', False) and user_preferences.get('email'):
                results['email'] = self.send_email_alert(
                    user_preferences['email'],
                    title,
                    message
                )
            
            # Send push notification if enabled
            if user_preferences.get('push_enabled', False) and user_preferences.get('user_id'):
                results['push'] = self.send_push_notification(
                    user_preferences['user_id'],
                    title,
                    message
                )
            
            # Send SMS if enabled
            if user_preferences.get('sms_enabled', False) and user_preferences.get('phone'):
                results['sms'] = self.send_sms_alert(
                    user_preferences['phone'],
                    message
                )
            
            return results
            
        except Exception as e:
            logger.error(f"Error sending alert notifications: {str(e)}")
            return {'error': str(e)}
    
    def format_alert_message(self, alert_data: Dict[str, Any]) -> str:
        """Format alert message for notifications"""
        return f"""
🚨 STOCK ALERT 🚨

Store: {alert_data.get('store_name', 'Unknown')}
Shelf: {alert_data['shelf_name']}
Status: {alert_data['stock_level']}
Priority: {alert_data['priority']}

{alert_data['message']}

Occupancy Score: {alert_data['occupancy_score']:.3f}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please check and refill the shelf as needed.
        """.strip()
    
    def create_dashboard_notification(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create notification for dashboard/real-time updates"""
        return {
            'type': 'alert',
            'priority': alert_data['priority'],
            'title': f"Stock Alert: {alert_data['shelf_name']}",
            'message': alert_data['message'],
            'shelf_id': alert_data['shelf_id'],
            'shelf_name': alert_data['shelf_name'],
            'occupancy_score': alert_data['occupancy_score'],
            'stock_level': alert_data['stock_level'],
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
