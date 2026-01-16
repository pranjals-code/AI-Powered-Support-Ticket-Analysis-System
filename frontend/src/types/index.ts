export enum UserRole {
  ADMIN = 'ADMIN',
  AGENT = 'AGENT',
  MANAGER = 'MANAGER',
}

export enum TicketStatus {
  CREATED = 'CREATED',
  ASSIGNED = 'ASSIGNED',
  IN_PROGRESS = 'IN_PROGRESS',
  RESOLVED = 'RESOLVED',
  CLOSED = 'CLOSED',
}

export enum TicketPriority {
  LOW = 'LOW',
  MEDIUM = 'MEDIUM',
  HIGH = 'HIGH',
}

export enum TicketCategory {
  BILLING = 'BILLING',
  TECHNICAL = 'TECHNICAL',
  ACCOUNT = 'ACCOUNT',
  OTHER = 'OTHER',
}

export interface User {
  id: number;
  email: string;
  role: UserRole;
  name?: string;
  avatar?: string;
}

export interface Ticket {
  id: number;
  title: string;
  description: string;
  status: TicketStatus;
  priority?: TicketPriority;
  category?: TicketCategory;
  created_at: string;
  updated_at?: string;
  created_by?: number;
  assigned_agent_id?: number;
  creator?: User;
  assigned_agent?: User;
}

export interface TicketCreate {
  title: string;
  description: string;
}

export interface TicketUpdate {
  title?: string;
  description?: string;
  status?: TicketStatus;
  priority?: TicketPriority;
  category?: TicketCategory;
  assigned_agent_id?: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  role: UserRole;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface Comment {
  id: number;
  content: string;
  author: User;
  ticket_id: number;
  created_at: string;
  updated_at?: string;
  is_internal?: boolean;
}

export interface DashboardStats {
  total_tickets: number;
  open_tickets: number;
  in_progress_tickets: number;
  resolved_tickets: number;
  high_priority_tickets: number;
  my_tickets: number;
}

