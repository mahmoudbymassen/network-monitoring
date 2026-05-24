import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material';

import Dashboard from './components/Dashboard';
import TopologyMap from './components/TopologyMap';
import DevicesTable from './components/DevicesTable';
import AlertsPanel from './components/AlertsPanel';

function App() {
  return (
    <Router>
      <AppBar position="static" elevation={2}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            🖧 Network Infrastructure Monitoring
          </Typography>

          <Button color="inherit" component={Link} to="/">Dashboard</Button>
          <Button color="inherit" component={Link} to="/topology">Topology</Button>
          <Button color="inherit" component={Link} to="/devices">Devices</Button>
          <Button color="inherit" component={Link} to="/alerts">Alerts</Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4, mb: 6 }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/topology" element={<TopologyMap />} />
          <Route path="/devices" element={<DevicesTable />} />
          <Route path="/alerts" element={<AlertsPanel />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;