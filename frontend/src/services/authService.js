import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  verifyToken: async (token) => {
    // This would typically be a separate endpoint
    // For now, we'll try to get user info
    const response = await api.get('/api/auth/me');
    return response.data;
  },
};

export const storeService = {
  getStores: () => api.get('/api/stores'),
  getStore: (id) => api.get(`/api/stores/${id}`),
  createStore: (data) => api.post('/api/stores', data),
  updateStore: (id, data) => api.put(`/api/stores/${id}`, data),
  deleteStore: (id) => api.delete(`/api/stores/${id}`),
};

export const cameraService = {
  getCameras: (storeId) => api.get('/api/cameras', { params: { store_id: storeId } }),
  getCamera: (id) => api.get(`/api/cameras/${id}`),
  createCamera: (data) => api.post('/api/cameras', data),
  updateCamera: (id, data) => api.put(`/api/cameras/${id}`, data),
  deleteCamera: (id) => api.delete(`/api/cameras/${id}`),
  updateCameraStatus: (id, status) => api.put(`/api/cameras/${id}/status`, { status }),
};

export const shelfService = {
  getShelves: (cameraId) => api.get('/api/shelves', { params: { camera_id: cameraId } }),
  getShelf: (id) => api.get(`/api/shelves/${id}`),
  createShelf: (data) => api.post('/api/shelves', data),
  updateShelf: (id, data) => api.put(`/api/shelves/${id}`, data),
  deleteShelf: (id) => api.delete(`/api/shelves/${id}`),
};

export const alertService = {
  getAlerts: (params) => api.get('/api/alerts', { params }),
  getAlert: (id) => api.get(`/api/alerts/${id}`),
  acknowledgeAlert: (id) => api.post(`/api/alerts/${id}/acknowledge`),
  createAlert: (data) => api.post('/api/alerts', data),
};

export const analyticsService = {
  getDashboardAnalytics: (params) => api.get('/api/analytics/dashboard', { params }),
  getStoreAnalytics: (storeId, params) => api.get(`/api/analytics/stores/${storeId}`, { params }),
  getShelfAnalytics: (shelfId, params) => api.get(`/api/analytics/shelves/${shelfId}`, { params }),
};

export const cvService = {
  processFrame: (cameraId, imageFile) => {
    const formData = new FormData();
    formData.append('camera_id', cameraId);
    formData.append('file', imageFile);
    return api.post('/api/cv/process-frame', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  detectShelves: (cameraId, imageFile) => {
    const formData = new FormData();
    formData.append('camera_id', cameraId);
    formData.append('file', imageFile);
    return api.post('/api/cv/detect-shelves', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export default api;
