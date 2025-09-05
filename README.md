# Automated Stock Monitoring AI Camera System

A comprehensive full-stack application for automated stock monitoring using computer vision and AI.

## 🎯 Features

### Core Functionality
- **Automatic Shelf Detection**: AI-powered shelf detection using OpenCV and computer vision
- **Real-time Stock Monitoring**: Continuous monitoring of shelf stock levels
- **Smart Alerting System**: Intelligent alerts for empty or low-stock shelves
- **Live Camera Feeds**: Real-time video processing and analysis
- **Multi-store Support**: Manage multiple stores and camera locations

### Web Dashboard
- **Modern React Frontend**: Responsive, user-friendly interface
- **Real-time Updates**: WebSocket-based live updates
- **Analytics & Reports**: Comprehensive analytics and reporting
- **User Management**: Role-based access control
- **Mobile Responsive**: Works on all devices

### Computer Vision Features
- **Advanced CV Algorithms**: Multiple detection techniques for accuracy
- **Auto-calibration**: Automatic shelf region detection
- **Threshold Configuration**: Customizable empty/low stock thresholds
- **Multi-camera Support**: Handle multiple camera feeds simultaneously

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI Framework**: High-performance Python web framework
- **SQLAlchemy ORM**: Database management with PostgreSQL/SQLite
- **WebSocket Support**: Real-time communication
- **JWT Authentication**: Secure user authentication
- **RESTful API**: Comprehensive API for all operations

### Frontend (React)
- **React 18**: Modern React with hooks
- **Material-UI**: Beautiful, responsive UI components
- **React Query**: Efficient data fetching and caching
- **Socket.IO**: Real-time WebSocket communication
- **Recharts**: Interactive charts and analytics

### Computer Vision (OpenCV)
- **OpenCV**: Advanced computer vision processing
- **Multiple Detection Methods**: Edge detection, contour analysis, background subtraction
- **Real-time Processing**: Live video analysis
- **Configurable Parameters**: Adjustable sensitivity and thresholds

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- PostgreSQL (optional, SQLite by default)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Computer Vision System
```bash
cd cv_system
python enhanced_monitor.py
```

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd wallmart-project
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost/stockmonitor"
export SECRET_KEY="your-secret-key-here"

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 4. Computer Vision System
```bash
cd cv_system
pip install opencv-python numpy requests
python enhanced_monitor.py
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=sqlite:///./stock_monitor.db
SECRET_KEY=your-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Camera Configuration
- **Webcam**: Use camera ID (0, 1, 2, etc.)
- **RTSP Stream**: Use RTSP URL
- **Video File**: Use file path

## 🎮 Usage

### 1. Initial Setup
1. Register a new account or login
2. Create a store
3. Add cameras to your store
4. Configure shelf regions using the live monitoring interface

### 2. Monitoring
1. Go to Live Monitoring page
2. Select your camera
3. Start monitoring
4. The system will automatically detect empty shelves and send alerts

### 3. Analytics
- View dashboard for overview
- Check analytics for detailed insights
- Monitor alert history
- Track stock patterns

## 🔍 Computer Vision Details

### Detection Methods
1. **Edge Density Analysis**: Analyzes edge patterns in shelf regions
2. **Color Variance**: Measures color distribution changes
3. **Histogram Analysis**: Compares histogram variations
4. **Background Subtraction**: Detects foreground objects
5. **Contour Analysis**: Analyzes shape complexity
6. **Texture Analysis**: Measures surface texture patterns

### Automatic Shelf Detection
- Uses Canny edge detection
- Applies morphological operations
- Identifies rectangular regions
- Filters by aspect ratio and size
- Ranks by confidence score

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration

### Stores
- `GET /api/stores` - List stores
- `POST /api/stores` - Create store
- `GET /api/stores/{id}` - Get store details

### Cameras
- `GET /api/cameras` - List cameras
- `POST /api/cameras` - Add camera
- `PUT /api/cameras/{id}/status` - Update camera status

### Shelves
- `GET /api/shelves` - List shelves
- `POST /api/shelves` - Create shelf
- `DELETE /api/shelves/{id}` - Delete shelf

### Alerts
- `GET /api/alerts` - List alerts
- `POST /api/alerts/{id}/acknowledge` - Acknowledge alert

### Computer Vision
- `POST /api/cv/process-frame` - Process frame for analysis
- `POST /api/cv/detect-shelves` - Auto-detect shelves

## 🔔 Notification System

### Supported Channels
- **Email**: SMTP-based email notifications
- **Push Notifications**: Web push notifications
- **SMS**: SMS alerts (integration required)
- **WebSocket**: Real-time dashboard updates

### Alert Priorities
- **HIGH**: Critical empty shelves requiring immediate attention
- **MEDIUM**: Low stock levels
- **LOW**: General notifications

## 🛠️ Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🐳 Docker Deployment

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/stockmonitor
    depends_on:
      - db
  
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=stockmonitor
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 📈 Performance Optimization

### Backend
- Database indexing for fast queries
- Caching for frequently accessed data
- Async processing for CV operations
- Connection pooling

### Frontend
- Code splitting for faster loading
- Image optimization
- Lazy loading for components
- Service worker for offline support

### Computer Vision
- Multi-threading for parallel processing
- Frame skipping for performance
- Configurable processing intervals
- GPU acceleration support

## 🔐 Security

### Authentication
- JWT token-based authentication
- Role-based access control
- Password hashing with bcrypt
- Session management

### API Security
- CORS configuration
- Input validation
- Rate limiting
- SQL injection prevention

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please create an issue in the GitHub repository or contact the development team.

## 🚀 Future Enhancements

- **Mobile App**: Native mobile applications
- **AI/ML Integration**: Advanced machine learning models
- **Cloud Integration**: AWS/Azure cloud deployment
- **IoT Integration**: Integration with IoT sensors
- **Advanced Analytics**: Predictive analytics and forecasting
- **Multi-language Support**: Internationalization
- **Advanced Reporting**: Custom report generation
- **Integration APIs**: Third-party system integrations

---

**Made with ❤️ for modern retail automation**
