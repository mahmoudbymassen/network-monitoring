import React, { useEffect, useState } from 'react';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper, 
  Chip, 
  Typography,
  Button,
  Box 
} from '@mui/material';
import { networkApi } from '../services/api';
import { Appareil } from '../types';
import { saveAs } from 'file-saver';

const DevicesTable = () => {
  const [devices, setDevices] = useState<Appareil[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      const data = await networkApi.getAllDevices();
      setDevices(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error fetching devices:", error);
    } finally {
      setLoading(false);
    }
  };

  const exportToExcel = async () => {
    try {
      const response = await networkApi.exportToExcel();
      const blob = new Blob([response.data as BlobPart], { 
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
      });
      saveAs(blob, `Appareils_Réseau_${new Date().toISOString().slice(0,10)}.xlsx`);
      alert("✅ Exported to Excel successfully!");
    } catch (error) {
      alert("Export to Excel failed");
      console.error(error);
    }
  };

  const exportToCSV = async () => {
    try {
      const response = await networkApi.exportToCSV();
      const blob = new Blob([response.data as BlobPart], { 
        type: 'text/csv' 
      });
      saveAs(blob, `Appareils_Réseau_${new Date().toISOString().slice(0,10)}.csv`);
      alert("✅ Exported to CSV successfully!");
    } catch (error) {
      alert("Export to CSV failed");
      console.error(error);
    }
  };

  const getStatusColor = (status: string) => (status === 'en_ligne' ? 'success' : 'error');

  if (loading) return <Typography>Loading devices...</Typography>;

  return (
    <div>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">All Devices</Typography>
        
        <Box>
          <Button 
            variant="contained" 
            color="primary" 
            onClick={exportToExcel}
            sx={{ mr: 2 }}
          >
            Export to Excel
          </Button>
          <Button 
            variant="outlined" 
            onClick={exportToCSV}
          >
            Export to CSV
          </Button>
        </Box>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>IP Address</strong></TableCell>
              <TableCell>MAC Address</TableCell>
              <TableCell>Hostname</TableCell>
              <TableCell>Marque</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Floor</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {devices.map((device) => (
              <TableRow key={device.id}>
                <TableCell><strong>{device.adresse_ip}</strong></TableCell>
                <TableCell>{device.adresse_mac || '-'}</TableCell>
                <TableCell>{device.nom_hote || '-'}</TableCell>
                <TableCell>{device.marque || '-'}</TableCell>
                <TableCell>{device.type_appareil}</TableCell>
                <TableCell>{device.etage}</TableCell>
                <TableCell>
                  <Chip 
                    label={device.statut} 
                    color={getStatusColor(device.statut)} 
                    size="small"
                  />
                </TableCell>
                
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
};

export default DevicesTable;