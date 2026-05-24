import React, { useEffect, useState } from 'react';

import {
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  CircularProgress,
  Box
} from '@mui/material';

import {
  networkApi,
  DashboardData
} from '../services/api';

const Dashboard = () => {

  const [dashboard, setDashboard] =
    useState<DashboardData | null>(null);

  const [loading, setLoading] = useState(false);

  const [scanLoading, setScanLoading] = useState(false);

  const [error, setError] = useState<string | null>(null);


  // =========================
  // LOAD DASHBOARD
  // =========================

  const fetchDashboard = async () => {

  try {

    setLoading(true);
    setError(null);

    const response: any =
      await networkApi.getDashboard();

    console.log(
      "FULL DASHBOARD RESPONSE:",
      response
    );

    const dashboardData =
      response?.dashboard ||
      response?.data?.dashboard ||
      response;

    setDashboard(dashboardData);

  } catch (err) {

    console.error("Dashboard Error:", err);

    setError("Failed to load dashboard");

  } finally {

    setLoading(false);

  }
};


  // =========================
  // START NETWORK SCAN
  // =========================

  const startScan = async () => {

    try {

      setScanLoading(true);

      const response = await networkApi.startScan(
        "192.168.1.0/24",
        false
      );

      console.log("Scan Response:", response);

      await fetchDashboard();

      alert(`✅ ${response.devices_found} devices found`);

    } catch (error) {

      console.error(error);

      alert("❌ Scan failed");

    } finally {

      setScanLoading(false);

    }
  };


  // =========================
  // INITIAL LOAD
  // =========================

  useEffect(() => {
    fetchDashboard();
  }, []);


  // =========================
  // LOADING
  // =========================

  if (loading && !dashboard) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          mt: 10
        }}
      >
        <CircularProgress />
      </Box>
    );
  }


  // =========================
  // ERROR
  // =========================

  if (error) {
    return (
      <Typography color="error">
        {error}
      </Typography>
    );
  }


  // =========================
  // CARDS
  // =========================

  const cards = [
    {
      label: 'Total Devices',
      value: dashboard?.total_appareils || 0,
      bg: '#ffffff',
      color: '#000'
    },
    {
      label: 'Online',
      value: dashboard?.en_ligne || 0,
      bg: '#e8f5e9',
      color: 'green'
    },
    {
      label: 'Offline',
      value: dashboard?.hors_ligne || 0,
      bg: '#ffebee',
      color: 'red'
    },
    {
      label: 'Online Rate',
      value: `${dashboard?.pourcentage_en_ligne || 0}%`,
      bg: '#e3f2fd',
      color: '#1976d2'
    }
  ];


  // =========================
  // UI
  // =========================

  return (

    <Box sx={{ p: 4 }}>

      <Typography
        variant="h3"
        gutterBottom
        sx={{ mb: 4 }}
      >
        Network Dashboard
      </Typography>


      <Grid container spacing={3}>

        {cards.map((card, index) => (

          <Grid key={index} size={{ xs: 12, md: 3 }}>

            <Card
              elevation={4}
              sx={{
                borderRadius: 4,
                bgcolor: card.bg
              }}
            >

              <CardContent>

                <Typography
                  variant="h3"
                  sx={{
                    fontWeight: 'bold',
                    color: card.color
                  }}
                >
                  {card.value}
                </Typography>

                <Typography
                  variant="h6"
                  color="text.secondary"
                  sx={{ mt: 1 }}
                >
                  {card.label}
                </Typography>

              </CardContent>

            </Card>

          </Grid>

        ))}

      </Grid>


      <Box sx={{ mt: 5 }}>

        <Button
          variant="contained"
          size="large"
          onClick={fetchDashboard}
          disabled={loading}
          sx={{ mr: 2 }}
        >
          Refresh Dashboard
        </Button>


        <Button
          variant="contained"
          color="secondary"
          size="large"
          onClick={startScan}
          disabled={scanLoading}
        >

          {scanLoading
            ? "Scanning..."
            : "🔍 Start Network Scan"}

        </Button>

      </Box>

    </Box>
  );
};

export default Dashboard;