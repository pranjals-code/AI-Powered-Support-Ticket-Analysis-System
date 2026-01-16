import { TicketStatus } from '@/types';
import { Badge } from '@/components/ui/Badge';

interface StatusBadgeProps {
  status: TicketStatus;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const getVariant = (status: TicketStatus) => {
    switch (status) {
      case TicketStatus.CREATED:
        return 'default';
      case TicketStatus.ASSIGNED:
        return 'info';
      case TicketStatus.IN_PROGRESS:
        return 'warning';
      case TicketStatus.RESOLVED:
        return 'success';
      case TicketStatus.CLOSED:
        return 'default';
      default:
        return 'default';
    }
  };

  const formatStatus = (status: TicketStatus) => {
    return status.replace(/_/g, ' ');
  };

  return <Badge variant={getVariant(status)}>{formatStatus(status)}</Badge>;
};

