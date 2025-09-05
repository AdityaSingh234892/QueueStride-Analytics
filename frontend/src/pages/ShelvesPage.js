import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';

const ShelvesPage = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Shelves Management
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Box textAlign="center" py={4}>
          <Typography variant="h6" color="textSecondary">
            Shelf management features coming soon...
          </Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mt: 2 }}>
            This page will allow you to define shelf regions, configure stock thresholds, and manage shelf-specific settings.
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default ShelvesPage;
