#!/bin/bash

# Automated Stock Monitoring System Setup Script
# This script sets up the complete system for development

echo "🚀 Setting up Automated Stock Monitoring System..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm and try again."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Setup Backend
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOL
DATABASE_URL=sqlite:///./stock_monitor.db
SECRET_KEY=your-secret-key-change-this-in-production
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EOL
    echo "⚠️  Please update the .env file with your actual configuration!"
fi

cd ..

# Setup Frontend
echo "🎨 Setting up Frontend..."
cd frontend

# Install dependencies
npm install

cd ..

# Setup CV System
echo "📹 Setting up Computer Vision System..."
cd cv_system

# Install dependencies
pip install -r requirements.txt

cd ..

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To start the system:"
echo "1. Start the backend:"
echo "   cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo ""
echo "2. Start the frontend (in a new terminal):"
echo "   cd frontend && npm start"
echo ""
echo "3. Start the CV system (in a new terminal):"
echo "   cd cv_system && python enhanced_monitor.py"
echo ""
echo "🌐 The application will be available at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "📚 Check the README.md for more detailed instructions!"
