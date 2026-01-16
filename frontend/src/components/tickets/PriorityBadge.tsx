import { TicketPriority } from '@/types';
import { Badge } from '@/components/ui/Badge';

interface PriorityBadgeProps {
  priority: TicketPriority;
}

export const PriorityBadge: React.FC<PriorityBadgeProps> = ({ priority }) => {
  const getVariant = (priority: TicketPriority) => {
    switch (priority) {
      case TicketPriority.LOW:
        return 'success';
      case TicketPriority.MEDIUM:
        return 'warning';
      case TicketPriority.HIGH:
        return 'danger';
      default:
        return 'default';
    }
  };

  return <Badge variant={getVariant(priority)}>{priority}</Badge>;
};

