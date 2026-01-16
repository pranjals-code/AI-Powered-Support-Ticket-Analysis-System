import { apiClient } from './client';
import { DashboardStats } from '@/types';

export const dashboardApi = {
  // Get dashboard statistics
  getStats: async (): Promise<DashboardStats> => {
    const response = await apiClient.get('/analytics/dashboard');
    return response.data;
  },

  // Get ticket trends
  getTicketTrends: async (days: number = 30) => {
    const response = await apiClient.get('/analytics/trends', {
      params: { days },
    });
    return response.data;
  },

  // Get agent performance
  getAgentPerformance: async () => {
    const response = await apiClient.get('/analytics/agents');
    return response.data;
  },
};

