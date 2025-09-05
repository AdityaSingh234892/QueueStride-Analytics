# Project Structure

```
wallmart-project/
├── README.md                          # Comprehensive project documentation
├── docker-compose.yml                 # Docker composition for full stack
├── setup.sh                          # Linux/Mac setup script
├── setup.bat                         # Windows setup script
├── 
├── backend/                           # FastAPI Backend
│   ├── main.py                       # FastAPI application entry point
│   ├── models.py                     # SQLAlchemy database models
│   ├── schemas.py                    # Pydantic schemas for API
│   ├── database.py                   # Database configuration
│   ├── auth.py                       # Authentication logic
│   ├── cv_processor.py               # Computer vision processing
│   ├── notification_system.py        # Notification handling
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Backend container
│   └── .env                          # Environment variables (create)
│
├── frontend/                          # React Frontend
│   ├── package.json                  # Node.js dependencies
│   ├── public/
│   │   └── index.html                # HTML template
│   ├── src/
│   │   ├── App.js                    # Main React component
│   │   ├── index.js                  # React entry point
│   │   ├── index.css                 # Global styles
│   │   ├── components/
│   │   │   ├── Layout.js             # Main layout component
│   │   │   └── LoadingSpinner.js     # Loading component
│   │   ├── contexts/
│   │   │   ├── AuthContext.js        # Authentication context
│   │   │   └── SocketContext.js      # WebSocket context
│   │   ├── pages/
│   │   │   ├── LoginPage.js          # Login page
│   │   │   ├── RegisterPage.js       # Registration page
│   │   │   ├── Dashboard.js          # Main dashboard
│   │   │   ├── LiveMonitoringPage.js # Live monitoring interface
│   │   │   ├── StoresPage.js         # Stores management
│   │   │   ├── CamerasPage.js        # Cameras management
│   │   │   ├── ShelvesPage.js        # Shelves management
│   │   │   ├── AlertsPage.js         # Alerts management
│   │   │   ├── AnalyticsPage.js      # Analytics and reports
│   │   │   └── SettingsPage.js       # Settings page
│   │   └── services/
│   │       └── authService.js        # API services
│   ├── Dockerfile                    # Frontend container
│   └── nginx.conf                    # Nginx configuration
│
├── cv_system/                        # Computer Vision System
│   ├── enhanced_monitor.py           # Enhanced CV monitoring system
│   ├── requirements.txt              # CV dependencies
│   └── Dockerfile                    # CV container
│
├── Asm.py                            # Original simple CV implementation
└── Asm1.py                           # Original advanced CV implementation
```

## Key Components

### Backend (FastAPI)
- **Authentication**: JWT-based user authentication
- **Database**: SQLAlchemy ORM with PostgreSQL/SQLite
- **API**: RESTful API for all operations
- **WebSocket**: Real-time communication
- **CV Processing**: Computer vision analysis
- **Notifications**: Email, SMS, push notifications

### Frontend (React)
- **Modern UI**: Material-UI components
- **Real-time Updates**: WebSocket integration
- **Responsive Design**: Works on all devices
- **State Management**: React Query for data fetching
- **Authentication**: JWT token management
- **Live Monitoring**: Webcam and file upload support

### Computer Vision
- **OpenCV**: Advanced image processing
- **Multiple Algorithms**: Edge detection, contour analysis
- **Auto-detection**: Automatic shelf region detection
- **Real-time Processing**: Live video analysis
- **Configurable**: Adjustable parameters and thresholds

### Deployment
- **Docker**: Complete containerization
- **Docker Compose**: Multi-service orchestration
- **Nginx**: Production-ready web server
- **PostgreSQL**: Production database
- **Redis**: Caching and session management

## Getting Started

1. **Quick Setup**: Run `setup.bat` (Windows) or `setup.sh` (Linux/Mac)
2. **Manual Setup**: Follow the README.md instructions
3. **Docker**: Use `docker-compose up` for containerized deployment

## Features

- ✅ **User Authentication & Authorization**
- ✅ **Real-time Stock Monitoring**
- ✅ **Automatic Shelf Detection**
- ✅ **Smart Alerting System**
- ✅ **Live Camera Feeds**
- ✅ **Analytics Dashboard**
- ✅ **Multi-store Support**
- ✅ **Mobile Responsive**
- ✅ **WebSocket Real-time Updates**
- ✅ **Docker Deployment**

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Redis
- **Frontend**: React, Material-UI, Socket.IO, Recharts
- **Computer Vision**: OpenCV, NumPy, Python
- **Deployment**: Docker, Nginx, PostgreSQL
- **Authentication**: JWT, bcrypt
- **Real-time**: WebSocket, Socket.IO
