import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';

const CamerasPage = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Cameras Management
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Box textAlign="center" py={4}>
          <Typography variant="h6" color="textSecondary">
            Camera management features coming soon...
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
            This page will allow you to manage your cameras, configure RTSP streams, and monitor camera status.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default CamerasPage;
