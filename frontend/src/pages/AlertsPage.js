import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';

const AlertsPage = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Alerts Management
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Box textAlign="center" py={4}>
          <Typography variant="h6" color="textSecondary">
            Alert management features coming soon...
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
            This page will show all alerts, allow you to acknowledge them, and configure alert settings.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default AlertsPage;
