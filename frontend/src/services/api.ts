import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});


// ======================
// TYPES
// ======================

export interface DashboardData {
  total_appareils: number;
  en_ligne: number;
  hors_ligne: number;
  pourcentage_en_ligne: number;
}

export interface DashboardResponse {
  status: string;
  dashboard: DashboardData;
}

export interface Device {
  id: number;
  adresse_ip: string;
  adresse_mac?: string;
  marque?: string;
  statut?: string;
  type_appareil?: string;
}

export interface DevicesResponse {
  appareils: Device[];
}

export interface ScanResponse {
  status: string;
  message: string;
  devices_found: number;
  deep_scan_enabled: boolean;
}

export interface Alert {
  id: number;
  message?: string;
  severite?: string;
  type_alerte?: string;
}

export interface AlertsResponse {
  alertes: Alert[];
}

export interface TopologyNode {
  id: number | string;
  label?: string;
  ip?: string;
  adresse_ip?: string;
  status?: 'en_ligne' | 'hors_ligne';
  floor?: number;
  [key: string]: any;
}

export interface TopologyEdge {
  from: number | string;
  to: number | string;
  [key: string]: any;
}

export interface TopologyResponse {
  nodes?: TopologyNode[];
  edges?: TopologyEdge[];
  topology?: {
    nodes: TopologyNode[];
    edges: TopologyEdge[];
  };
}


// ======================
// API
// ======================

export const networkApi = {
// DASHBOARD
getDashboard: async (): Promise<DashboardResponse> => {
  const res = await api.get<DashboardResponse>('/api/dashboard/');
  return res.data;
},

// DEVICES
getAllDevices: async (): Promise<DevicesResponse> => {
  const res = await api.get<DevicesResponse>('/api/appareils/');
  return res.data;
},

// SCAN
startScan: async (
  ipRange = "192.168.1.0/24",
  deepScan = false
): Promise<ScanResponse> => {

  const res = await api.post<ScanResponse>(
    '/api/scan/start',
    {},
    {
      params: {
        ip_range: ipRange,
        deep_scan: deepScan
      }
    }
  );

  return res.data;
},

// TOPOLOGY
getTopology: async (): Promise<TopologyResponse> => {
  const res = await api.get<TopologyResponse>('/api/topology/');
  // Return the full response so we can handle both structures safely
  return res.data;
},

// ALERTS
getAllAlerts: async (): Promise<AlertsResponse> => {
  const res = await api.get<AlertsResponse>('/api/alertes/');
  return res.data;
},

acknowledgeAlert: async (id: number): Promise<Alert> => {
  const res = await api.put<Alert>(
    `/api/alertes/${id}/acknowledge`
  );

  return res.data;
},

  // EXPORTS
  exportToExcel: async () => {
    return api.get('/api/export/devices/excel', {
      responseType: 'blob'
    });
  },

  exportToCSV: async () => {
    return api.get('/api/export/devices/csv', {
      responseType: 'blob'
    });
  },
};