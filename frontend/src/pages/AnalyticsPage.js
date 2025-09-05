import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';

const AnalyticsPage = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Analytics & Reports
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Box textAlign="center" py={4}>
          <Typography variant="h6" color="textSecondary">
            Analytics features coming soon...
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
            This page will provide detailed analytics, reports, and insights about your store performance and stock levels.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default AnalyticsPage;
