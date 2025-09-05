from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: str = "manager"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Store schemas
class StoreBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class StoreCreate(StoreBase):
    pass

class StoreResponse(StoreBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Camera schemas
class CameraBase(BaseModel):
    name: str
    location: Optional[str] = None
    rtsp_url: Optional[str] = None
    ip_address: Optional[str] = None
    status: str = "active"

class CameraCreate(CameraBase):
    store_id: int

class CameraResponse(CameraBase):
    id: int
    store_id: int
    created_at: datetime
    last_seen: datetime
    
    class Config:
        from_attributes = True

# Shelf schemas
class ShelfBase(BaseModel):
    name: str
    region: List[int]  # [x, y, width, height]
    product_category: Optional[str] = None
    expected_stock_level: str = "high"
    empty_threshold: float = 0.15

class ShelfCreate(ShelfBase):
    camera_id: int

class ShelfResponse(ShelfBase):
    id: int
    camera_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Alert schemas
class AlertBase(BaseModel):
    priority: str
    message: str
    occupancy_score: float

class AlertCreate(AlertBase):
    shelf_id: int

class AlertResponse(AlertBase):
    id: int
    shelf_id: int
    acknowledged: bool
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Stock level schemas
class StockLevelBase(BaseModel):
    occupancy_score: float
    stock_status: str

class StockLevelCreate(StockLevelBase):
    shelf_id: int

class StockLevelResponse(StockLevelBase):
    id: int
    shelf_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Notification settings schemas
class NotificationSettingsBase(BaseModel):
    email_enabled: bool = True
    sms_enabled: bool = False
    push_enabled: bool = True
    alert_frequency: str = "immediate"

class NotificationSettingsCreate(NotificationSettingsBase):
    user_id: int

class NotificationSettingsResponse(NotificationSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Analytics schemas
class DashboardAnalytics(BaseModel):
    stores_count: int
    cameras_count: int
    shelves_count: int
    total_alerts: int
    high_priority_alerts: int
    alerts_by_day: List[Dict[str, Any]]
