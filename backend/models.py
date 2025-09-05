from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(String, default="manager")  # manager, admin, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    stores = relationship("Store", back_populates="owner")
    acknowledged_alerts = relationship("Alert", foreign_keys="Alert.acknowledged_by", back_populates="acknowledged_by_user")

class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="stores")
    cameras = relationship("Camera", back_populates="store")

class Camera(Base):
    __tablename__ = "cameras"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    rtsp_url = Column(String)
    ip_address = Column(String)
    status = Column(String, default="active")  # active, inactive, maintenance
    store_id = Column(Integer, ForeignKey("stores.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    store = relationship("Store", back_populates="cameras")
    shelves = relationship("Shelf", back_populates="camera")

class Shelf(Base):
    __tablename__ = "shelves"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    region = Column(JSON)  # [x, y, width, height]
    product_category = Column(String)
    expected_stock_level = Column(String, default="high")  # high, medium, low
    empty_threshold = Column(Float, default=0.15)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    camera = relationship("Camera", back_populates="shelves")
    alerts = relationship("Alert", back_populates="shelf")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    shelf_id = Column(Integer, ForeignKey("shelves.id"))
    priority = Column(String)  # HIGH, MEDIUM, LOW
    message = Column(String)
    occupancy_score = Column(Float)
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime)
    acknowledged_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    shelf = relationship("Shelf", back_populates="alerts")
    acknowledged_by_user = relationship("User", foreign_keys=[acknowledged_by], back_populates="acknowledged_alerts")

class StockLevel(Base):
    __tablename__ = "stock_levels"
    
    id = Column(Integer, primary_key=True, index=True)
    shelf_id = Column(Integer, ForeignKey("shelves.id"))
    occupancy_score = Column(Float)
    stock_status = Column(String)  # EMPTY, LOW, MEDIUM, HIGH
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    shelf = relationship("Shelf")

class NotificationSettings(Base):
    __tablename__ = "notification_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    push_enabled = Column(Boolean, default=True)
    alert_frequency = Column(String, default="immediate")  # immediate, hourly, daily
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
