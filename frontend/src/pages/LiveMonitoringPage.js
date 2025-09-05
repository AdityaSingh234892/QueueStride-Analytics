import React, { useState, useRef, useCallback } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  Chip,
  IconButton,
  Tooltip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  PlayArrow,
  Pause,
  Stop,
  CameraAlt,
  Upload,
  Refresh,
  Fullscreen,
  Settings,
} from '@mui/icons-material';
import Webcam from 'react-webcam';
import { useDropzone } from 'react-dropzone';
import { useQuery } from 'react-query';
import { cameraService, cvService } from '../services/authService';
import { useSocket } from '../contexts/SocketContext';

const LiveMonitoringPage = () => {
  const [selectedCamera, setSelectedCamera] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentFrame, setCurrentFrame] = useState(null);
  const [analysisResults, setAnalysisResults] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [useWebcam, setUseWebcam] = useState(true);
  const webcamRef = useRef(null);
  const { connected } = useSocket();

  const { data: cameras, isLoading: camerasLoading } = useQuery(
    'cameras',
    () => cameraService.getCameras(),
    {
      select: (response) => response.data,
    }
  );

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        setCurrentFrame(reader.result);
        processFrame(file);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif']
    },
    multiple: false,
  });

  const captureFrame = useCallback(() => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setCurrentFrame(imageSrc);
      
      // Convert data URL to blob for processing
      fetch(imageSrc)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], 'webcam-capture.jpg', { type: 'image/jpeg' });
          processFrame(file);
        });
    }
  }, [webcamRef]);

  const processFrame = async (imageFile) => {
    if (!selectedCamera) {
      alert('Please select a camera first');
      return;
    }

    setProcessing(true);
    try {
      const response = await cvService.processFrame(selectedCamera, imageFile);
      setAnalysisResults(response.data.results);
    } catch (error) {
      console.error('Error processing frame:', error);
      alert('Error processing frame');
    } finally {
      setProcessing(false);
    }
  };

  const startStreaming = () => {
    setIsStreaming(true);
    // In a real implementation, this would start the video stream processing
    // For now, we'll just enable the webcam
  };

  const stopStreaming = () => {
    setIsStreaming(false);
    setAnalysisResults([]);
  };

  const autoDetectShelves = async () => {
    if (!currentFrame || !selectedCamera) {
      alert('Please capture a frame and select a camera first');
      return;
    }

    setProcessing(true);
    try {
      // Convert data URL to blob
      const blob = await fetch(currentFrame).then(res => res.blob());
      const file = new File([blob], 'frame.jpg', { type: 'image/jpeg' });
      
      const response = await cvService.detectShelves(selectedCamera, file);
      console.log('Detected shelves:', response.data.detected_shelves);
      // Handle detected shelves - you might want to add them to the database
      alert(`Detected ${response.data.detected_shelves.length} potential shelves`);
    } catch (error) {
      console.error('Error detecting shelves:', error);
      alert('Error detecting shelves');
    } finally {
      setProcessing(false);
    }
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Live Monitoring
      </Typography>

      {/* Connection Status */}
      <Alert 
        severity={connected ? 'success' : 'warning'} 
        sx={{ mb: 3 }}
      >
        {connected ? 'Connected to monitoring system' : 'Disconnected from monitoring system'}
      </Alert>

      <Grid container spacing={3}>
        {/* Camera Controls */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Camera Controls
            </Typography>
            
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Select Camera</InputLabel>
              <Select
                value={selectedCamera}
                onChange={(e) => setSelectedCamera(e.target.value)}
                label="Select Camera"
              >
                {cameras?.map((camera) => (
                  <MenuItem key={camera.id} value={camera.id}>
                    {camera.name} - {camera.location}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Box display="flex" gap={1} mb={2}>
              <Button
                variant={useWebcam ? 'contained' : 'outlined'}
                onClick={() => setUseWebcam(true)}
                startIcon={<CameraAlt />}
              >
                Webcam
              </Button>
              <Button
                variant={!useWebcam ? 'contained' : 'outlined'}
                onClick={() => setUseWebcam(false)}
                startIcon={<Upload />}
              >
                Upload
              </Button>
            </Box>

            <Box display="flex" gap={1} mb={2}>
              <Button
                variant="contained"
                color="primary"
                onClick={isStreaming ? stopStreaming : startStreaming}
                startIcon={isStreaming ? <Pause /> : <PlayArrow />}
                disabled={!selectedCamera}
              >
                {isStreaming ? 'Stop' : 'Start'}
              </Button>
              <Button
                variant="outlined"
                onClick={captureFrame}
                startIcon={<CameraAlt />}
                disabled={!useWebcam || !selectedCamera}
              >
                Capture
              </Button>
            </Box>

            <Box display="flex" gap={1}>
              <Button
                variant="outlined"
                onClick={autoDetectShelves}
                startIcon={<Settings />}
                disabled={!currentFrame || processing}
              >
                Auto Detect Shelves
              </Button>
              <Tooltip title="Refresh">
                <IconButton onClick={() => window.location.reload()}>
                  <Refresh />
                </IconButton>
              </Tooltip>
            </Box>
          </Paper>

          {/* Analysis Results */}
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Analysis Results
            </Typography>
            {processing && (
              <Box display="flex" alignItems="center" gap={2}>
                <CircularProgress size={20} />
                <Typography>Processing frame...</Typography>
              </Box>
            )}
            {analysisResults.length > 0 ? (
              <Box>
                {analysisResults.map((result, index) => (
                  <Card key={index} sx={{ mb: 1 }}>
                    <CardContent sx={{ py: 1 }}>
                      <Box display="flex" justifyContent="space-between" alignItems="center">
                        <Typography variant="subtitle2">
                          {result.shelf_name}
                        </Typography>
                        <Chip
                          label={result.stock_level}
                          color={
                            result.stock_level === 'EMPTY' ? 'error' :
                            result.stock_level === 'LOW' ? 'warning' :
                            result.stock_level === 'MEDIUM' ? 'info' : 'success'
                          }
                          size="small"
                        />
                      </Box>
                      <Typography variant="body2" color="textSecondary">
                        Score: {result.occupancy_score?.toFixed(3)}
                      </Typography>
                      {result.needs_alert && (
                        <Alert severity="error" sx={{ mt: 1 }}>
                          {result.message}
                        </Alert>
                      )}
                    </CardContent>
                  </Card>
                ))}
              </Box>
            ) : (
              <Typography color="textSecondary">
                No analysis results yet. Capture a frame to start analysis.
              </Typography>
            )}
          </Paper>
        </Grid>

        {/* Video/Image Display */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Live Feed
            </Typography>
            
            <Box
              sx={{
                position: 'relative',
                border: '2px dashed #ccc',
                borderRadius: 1,
                minHeight: 400,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: '#f5f5f5',
              }}
            >
              {useWebcam ? (
                <>
                  <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    width="100%"
                    height="auto"
                    style={{
                      maxWidth: '100%',
                      maxHeight: '400px',
                      objectFit: 'contain',
                    }}
                  />
                  {isStreaming && (
                    <Box
                      sx={{
                        position: 'absolute',
                        top: 10,
                        left: 10,
                        backgroundColor: 'rgba(0,0,0,0.7)',
                        color: 'white',
                        padding: '4px 8px',
                        borderRadius: 1,
                        fontSize: '0.8rem',
                      }}
                    >
                      🔴 LIVE
                    </Box>
                  )}
                </>
              ) : (
                <Box
                  {...getRootProps()}
                  sx={{
                    width: '100%',
                    height: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    cursor: 'pointer',
                    minHeight: 400,
                  }}
                >
                  <input {...getInputProps()} />
                  {currentFrame ? (
                    <img
                      src={currentFrame}
                      alt="Uploaded frame"
                      style={{
                        maxWidth: '100%',
                        maxHeight: '400px',
                        objectFit: 'contain',
                      }}
                    />
                  ) : (
                    <Box textAlign="center">
                      <Upload sx={{ fontSize: 48, color: '#ccc', mb: 2 }} />
                      <Typography>
                        {isDragActive
                          ? 'Drop the image here...'
                          : 'Drag & drop an image here, or click to select'}
                      </Typography>
                    </Box>
                  )}
                </Box>
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default LiveMonitoringPage;
