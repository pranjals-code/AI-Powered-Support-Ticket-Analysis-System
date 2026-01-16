import { apiClient } from './client';
import { LoginCredentials, RegisterData, AuthResponse } from '@/types';

export const authApi = {
  // Login user
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  },

  // Register new user
  register: async (data: RegisterData): Promise<{ message: string; user_id: number }> => {
    const response = await apiClient.post('/auth/signup', data);
    return response.data;
  },

  // Logout (clear local storage)
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

