import { apiClient } from './client';
import { Ticket, TicketCreate, TicketUpdate, TicketStatus } from '@/types';

export const ticketsApi = {
  // Get all tickets
  getAll: async (params?: {
    page?: number;
    size?: number;
    status?: TicketStatus;
    search?: string;
  }): Promise<Ticket[]> => {
    const response = await apiClient.get('/tickets', { params });
    return response.data;
  },

  // Get single ticket by ID
  getById: async (id: number): Promise<Ticket> => {
    const response = await apiClient.get(`/tickets/${id}`);
    return response.data;
  },

  // Create new ticket
  create: async (data: TicketCreate): Promise<Ticket> => {
    const response = await apiClient.post('/tickets', data);
    return response.data;
  },

  // Update ticket
  update: async (id: number, data: TicketUpdate): Promise<Ticket> => {
    const response = await apiClient.patch(`/tickets/${id}`, data);
    return response.data;
  },

  // Update ticket status
  updateStatus: async (id: number, status: TicketStatus): Promise<Ticket> => {
    const response = await apiClient.patch(`/tickets/${id}/status`, { status });
    return response.data;
  },

  // Delete ticket
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/tickets/${id}`);
  },

  // Assign ticket to agent
  assignTicket: async (id: number, agentId: number): Promise<Ticket> => {
    const response = await apiClient.patch(`/tickets/${id}/assign`, { agent_id: agentId });
    return response.data;
  },
};

