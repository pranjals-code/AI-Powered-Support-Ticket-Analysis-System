import { formatDistanceToNow, format } from 'date-fns';

export function formatDate(date: string | Date): string {
  return format(new Date(date), 'MMM dd, yyyy');
}

export function formatDateTime(date: string | Date): string {
  return format(new Date(date), 'MMM dd, yyyy HH:mm');
}

export function formatRelativeTime(date: string | Date): string {
  return formatDistanceToNow(new Date(date), { addSuffix: true });
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    CREATED: 'bg-gray-500',
    ASSIGNED: 'bg-blue-500',
    IN_PROGRESS: 'bg-yellow-500',
    RESOLVED: 'bg-green-500',
    CLOSED: 'bg-gray-700',
  };
  return colors[status] || 'bg-gray-500';
}

export function getPriorityColor(priority: string): string {
  const colors: Record<string, string> = {
    LOW: 'bg-green-500',
    MEDIUM: 'bg-yellow-500',
    HIGH: 'bg-red-500',
  };
  return colors[priority] || 'bg-gray-500';
}

export function getStatusTextColor(status: string): string {
  const colors: Record<string, string> = {
    CREATED: 'text-gray-700',
    ASSIGNED: 'text-blue-700',
    IN_PROGRESS: 'text-yellow-700',
    RESOLVED: 'text-green-700',
    CLOSED: 'text-gray-800',
  };
  return colors[status] || 'text-gray-700';
}

export function getPriorityTextColor(priority: string): string {
  const colors: Record<string, string> = {
    LOW: 'text-green-700',
    MEDIUM: 'text-yellow-700',
    HIGH: 'text-red-700',
  };
  return colors[priority] || 'text-gray-700';
}

