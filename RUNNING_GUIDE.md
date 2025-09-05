# Running the Automated Stock Monitoring AI Camera System

## Quick Start Guide

### Prerequisites
- Python 3.8+ installed
- OpenCV and required packages installed
- (Optional) Node.js for React frontend

### Option 1: Manual Start (Recommended)

1. **Start Backend Server**
   ```bash
   cd backend
   python main.py
   ```
   - Server will start on http://localhost:8000
   - API documentation: http://localhost:8000/docs

2. **Start CV System**
   ```bash
   cd cv_system
   python enhanced_monitor.py
   ```
   - Will open camera feed and start monitoring
   - Press 'q' to quit, 's' to toggle setup mode

3. **Test Original Script**
   ```bash
   python Asm1.py
   ```
   - Runs the original OpenCV shelf monitoring
   - Uses webcam or video file

4. **Open Web Client**
   - Open `simple-client.html` in your browser
   - Or use the system runner: `python run_components.py`

### Option 2: Batch File (Windows)
```bash
run_system.bat
```
This will start all components in separate windows.

### Option 3: Interactive Runner
```bash
python run_components.py
```
Choose components to start from an interactive menu.

## System Components

### Backend Server (FastAPI)
- **URL**: http://localhost:8000
- **Features**:
  - REST API for inventory management
  - User authentication
  - WebSocket for real-time updates
  - Database for storing alerts and analytics
  - Integration with CV system

### CV System (OpenCV + AI)
- **Enhanced Monitor**: Advanced shelf detection and monitoring
- **Original Script**: Basic shelf monitoring from Asm1.py
- **Features**:
  - Real-time shelf status detection
  - Product counting and categorization
  - Empty shelf alerts
  - Integration with backend API

### Web Interface
- **Simple Client**: `simple-client.html` - Basic testing interface
- **React Frontend**: Full dashboard (requires Node.js)

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Stores & Cameras
- `GET /api/stores` - List stores
- `POST /api/stores` - Create store
- `GET /api/cameras` - List cameras
- `POST /api/cameras` - Add camera

### Monitoring
- `GET /api/alerts` - Get alerts
- `POST /api/alerts` - Create alert
- `GET /api/analytics` - Get analytics data

### Real-time
- `WebSocket /ws` - Real-time updates

## Configuration

### Backend Configuration
Edit `backend/.env` (create if not exists):
```env
DATABASE_URL=sqlite:///./stock_monitor.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### CV System Configuration
Edit `cv_system/.env` (create if not exists):
```env
API_BASE_URL=http://localhost:8000
CAMERA_ID=0
VIDEO_FILE_PATH=path/to/video.mp4
```

## Testing

### Test Backend
```bash
python test_backend.py
```

### Test System
```bash
python test_system.py
```

### Manual Testing
1. Open `simple-client.html`
2. Test registration/login
3. Create a store
4. Add a camera
5. View analytics

## Troubleshooting

### Common Issues

1. **Backend won't start**
   - Check if Python packages are installed: `pip install -r backend/requirements.txt`
   - Verify port 8000 is available

2. **CV System camera error**
   - Check if camera is connected and accessible
   - Try different camera IDs (0, 1, 2...)
   - Use a video file instead of camera

3. **OpenCV issues**
   - Install OpenCV: `pip install opencv-python`
   - For conda: `conda install opencv`

4. **Frontend not working**
   - Install Node.js from https://nodejs.org/
   - Run `npm install` in frontend directory
   - Run `npm start` to start React app

### Debug Mode
Start backend with debug logging:
```bash
cd backend
python main.py --log-level debug
```

## Docker Deployment (Optional)

Build and run with Docker:
```bash
docker-compose up --build
```

This will start all components in containers.

## Video Sources

The system supports:
- Webcam (camera_id=0, 1, 2...)
- Video files (MP4, AVI, etc.)
- RTSP streams
- IP cameras

## Next Steps

1. **Add more cameras**: Configure multiple camera feeds
2. **Integrate inventory**: Connect to existing inventory systems
3. **Mobile app**: Add mobile notifications
4. **Advanced AI**: Implement product recognition
5. **Cloud deployment**: Deploy to AWS/Azure/GCP

## Support

For issues or questions:
1. Check the logs in terminal outputs
2. Verify all dependencies are installed
3. Test individual components first
4. Check the API documentation at http://localhost:8000/docs
