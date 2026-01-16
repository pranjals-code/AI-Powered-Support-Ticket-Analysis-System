import { Ticket } from '@/types';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { StatusBadge } from './StatusBadge';
import { PriorityBadge } from './PriorityBadge';
import { formatRelativeTime } from '@/utils/format';
import { User, Calendar } from 'lucide-react';

interface TicketCardProps {
  ticket: Ticket;
  onClick?: () => void;
}

export const TicketCard: React.FC<TicketCardProps> = ({ ticket, onClick }) => {
  return (
    <Card hover onClick={onClick} className="cursor-pointer">
      <CardHeader>
        <div className="flex justify-between items-start gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-sm font-medium text-gray-500">#{ticket.id}</span>
              <StatusBadge status={ticket.status} />
              {ticket.priority && <PriorityBadge priority={ticket.priority} />}
            </div>
            <h3 className="text-lg font-semibold text-gray-900">{ticket.title}</h3>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-gray-600 mb-4 line-clamp-2">{ticket.description}</p>
        <div className="flex flex-wrap gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            <span>{formatRelativeTime(ticket.created_at)}</span>
          </div>
          {ticket.category && (
            <div className="flex items-center gap-1">
              <span className="font-medium">{ticket.category}</span>
            </div>
          )}
          {ticket.assigned_agent && (
            <div className="flex items-center gap-1">
              <User className="w-4 h-4" />
              <span>Assigned</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

