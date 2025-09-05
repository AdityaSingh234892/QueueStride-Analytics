import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Alert,
  Chip,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  TrendingUp,
  Store,
  Videocam,
  Inventory,
  NotificationsActive,
  Warning,
  CheckCircle,
  Error,
  Refresh,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { useQuery } from 'react-query';
import { analyticsService } from '../services/authService';
import { useSocket } from '../contexts/SocketContext';
import { format } from 'date-fns';

const Dashboard = () => {
  const [refreshKey, setRefreshKey] = useState(0);
  const { alerts, connected } = useSocket();

  const { data: dashboardData, isLoading, error, refetch } = useQuery(
    ['dashboard', refreshKey],
    () => analyticsService.getDashboardAnalytics({ days: 7 }),
    {
      refetchInterval: 30000, // Refetch every 30 seconds
      select: (response) => response.data,
    }
  );

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1);
    refetch();
  };

  const recentAlerts = alerts.slice(0, 5);
  const highPriorityAlerts = alerts.filter(alert => alert.priority === 'HIGH').length;

  if (isLoading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <LinearProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="error">
          Failed to load dashboard data. Please try again.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={4}>
        <Typography variant="h4" component="h1">
          Dashboard
        </Typography>
        <Box display="flex" alignItems="center" gap={2}>
          <Chip
            label={connected ? 'Live' : 'Offline'}
            color={connected ? 'success' : 'error'}
            size="small"
          />
          <Tooltip title="Refresh Dashboard">
            <IconButton onClick={handleRefresh}>
              <Refresh />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* High Priority Alerts */}
      {highPriorityAlerts > 0 && (
        <Alert 
          severity="error" 
          sx={{ mb: 3 }}
          icon={<Warning />}
        >
          You have {highPriorityAlerts} high priority alerts that need immediate attention!
        </Alert>
      )}

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card className="dashboard-card">
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Stores
                  </Typography>
                  <Typography variant="h4">
                    {dashboardData?.stores_count || 0}
                  </Typography>
                </Box>
                <Store color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card className="dashboard-card">
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Active Cameras
                  </Typography>
                  <Typography variant="h4">
                    {dashboardData?.cameras_count || 0}
                  </Typography>
                </Box>
                <Videocam color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card className="dashboard-card">
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Monitored Shelves
                  </Typography>
                  <Typography variant="h4">
                    {dashboardData?.shelves_count || 0}
                  </Typography>
                </Box>
                <Inventory color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card className="dashboard-card">
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Alerts (7 days)
                  </Typography>
                  <Typography variant="h4" color={highPriorityAlerts > 0 ? 'error' : 'primary'}>
                    {dashboardData?.total_alerts || 0}
                  </Typography>
                </Box>
                <NotificationsActive 
                  color={highPriorityAlerts > 0 ? 'error' : 'primary'} 
                  sx={{ fontSize: 40 }} 
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Alerts Over Time (7 Days)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={dashboardData?.alerts_by_day || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={(value) => format(new Date(value), 'MMM dd')}
                />
                <YAxis />
                <RechartsTooltip 
                  labelFormatter={(value) => format(new Date(value), 'MMM dd, yyyy')}
                />
                <Line type="monotone" dataKey="alerts" stroke="#8884d8" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Alert Priority Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={[
                { name: 'High', value: dashboardData?.high_priority_alerts || 0, fill: '#f44336' },
                { name: 'Medium', value: (dashboardData?.total_alerts || 0) - (dashboardData?.high_priority_alerts || 0), fill: '#ff9800' },
                { name: 'Low', value: 0, fill: '#4caf50' },
              ]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <RechartsTooltip />
                <Bar dataKey="value" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent Alerts */}
      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Recent Alerts
        </Typography>
        {recentAlerts.length === 0 ? (
          <Box display="flex" alignItems="center" justifyContent="center" py={4}>
            <CheckCircle color="success" sx={{ mr: 1 }} />
            <Typography color="textSecondary">
              No recent alerts. All systems are running smoothly!
            </Typography>
          </Box>
        ) : (
          <Box>
            {recentAlerts.map((alert, index) => (
              <Box 
                key={index} 
                display="flex" 
                alignItems="center" 
                justifyContent="space-between"
                py={2}
                borderBottom={index < recentAlerts.length - 1 ? '1px solid #eee' : 'none'}
              >
                <Box display="flex" alignItems="center">
                  {alert.priority === 'HIGH' ? (
                    <Error color="error" sx={{ mr: 2 }} />
                  ) : (
                    <Warning color="warning" sx={{ mr: 2 }} />
                  )}
                  <Box>
                    <Typography variant="subtitle1">
                      {alert.title}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {alert.message}
                    </Typography>
                  </Box>
                </Box>
                <Box textAlign="right">
                  <Chip 
                    label={alert.priority} 
                    color={alert.priority === 'HIGH' ? 'error' : 'warning'}
                    size="small"
                  />
                  <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                    {format(new Date(alert.timestamp), 'MMM dd, HH:mm')}
                  </Typography>
                </Box>
              </Box>
            ))}
          </Box>
        )}
      </Paper>
    </Container>
  );
};

export default Dashboard;
