import { apiClient } from './client';
import axios from 'axios';

const BACKEND_URL = 'http://localhost:8000';

export const securityApi = {
  // Yangi AI Chat API
  async aiChat(text) {
    try {
      const response = await axios.post(`${BACKEND_URL}/ai/chat`, { text });
      return response.data;
    } catch (error) {
      console.error('AI API error:', error);
      return { response: "AI SERVER OFFLINE. Iltimos, Python backendni ishga tushiring." };
    }
  },

  getHealth() {
    return apiClient.get('/health');
  },
  getDashboard() {
    return apiClient.get('/dashboard');
  },
  getModule(moduleName) {
    return apiClient.get(`/modules/${encodeURIComponent(moduleName)}`);
  },
  startScan(mode = 'quick') {
    return apiClient.post('/scan', { mode });
  },
  blockIp(ip) {
    return apiClient.post('/block', { ip });
  },
  getAlerts(live = false) {
    return apiClient.get(`/alerts?live=${live ? 'true' : 'false'}`);
  },
  isolateIncident(incidentId, payload = {}) {
    return apiClient.post(`/incidents/${encodeURIComponent(incidentId)}/isolate`, payload);
  },
  getAttackMap() {
    return apiClient.get('/attack-map');
  }
};
