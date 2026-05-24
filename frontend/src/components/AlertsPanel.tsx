import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Chip, Button } from '@mui/material';
import { networkApi } from '../services/api';

interface Alert {
  id: number;
  type_alerte: string;
  severite: string;
  message: string;
  date_creation: string;
  accusee: boolean;
}

const AlertsPanel = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
  }, []);

  const fetchAlerts = async () => {
    try {
      const data = await networkApi.getAllAlerts();
      setAlerts(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error fetching alerts:", error);
      setAlerts([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAcknowledge = async (id: number) => {
    try {
      await networkApi.acknowledgeAlert(id);
      fetchAlerts();
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) return <Typography>Loading alerts...</Typography>;

  return (
    <div>
      <Typography variant="h5" gutterBottom>Recent Alerts</Typography>
      
      {alerts.length === 0 && <Typography>No alerts found.</Typography>}

      {alerts.map((alert) => (
        <Card key={alert.id} sx={{ mb: 2 }}>
          <CardContent>
            <Chip 
              label={alert.type_alerte} 
              color={alert.severite === 'elevee' ? 'error' : 'warning'} 
              sx={{ mb: 1 }}
            />
            <Typography variant="body1">{alert.message}</Typography>
            <Typography variant="caption" color="textSecondary">
              {new Date(alert.date_creation).toLocaleString()}
            </Typography>
            
            {!alert.accusee && (
              <Button 
                variant="outlined" 
                size="small" 
                onClick={() => handleAcknowledge(alert.id)}
                sx={{ mt: 1 }}
              >
                Mark as Read
              </Button>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default AlertsPanel;