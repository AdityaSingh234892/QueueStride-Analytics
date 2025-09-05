import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';

const SettingsPage = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Settings
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Box textAlign="center" py={4}>
          <Typography variant="h6" color="textSecondary">
            Settings features coming soon...
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
            This page will allow you to configure system settings, notification preferences, and user management.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default SettingsPage;
