import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { StatusBadge } from '@/components/tickets/StatusBadge';
import { PriorityBadge } from '@/components/tickets/PriorityBadge';
import { ArrowLeft, Calendar, User, Tag, Edit, Trash2 } from 'lucide-react';
import { formatDateTime, formatRelativeTime } from '@/utils/format';
import { TicketStatus, Ticket } from '@/types';
import { ticketsApi } from '@/api/tickets';

export const TicketDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [isUpdating, setIsUpdating] = useState(false);

  // Fetch ticket from API
  useEffect(() => {
    const fetchTicket = async () => {
      if (!id) return;
      
      try {
        setIsLoading(true);
        const data = await ticketsApi.getById(Number(id));
        setTicket(data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to load ticket');
      } finally {
        setIsLoading(false);
      }
    };

    fetchTicket();
  }, [id]);

  const handleStatusChange = async (newStatus: string) => {
    if (!id) return;
    
    setIsUpdating(true);
    
    try {
      const updatedTicket = await ticketsApi.updateStatus(Number(id), newStatus as TicketStatus);
      setTicket(updatedTicket);
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to update status');
    } finally {
      setIsUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (!id) return;
    
    if (window.confirm('Are you sure you want to delete this ticket?')) {
      try {
        await ticketsApi.delete(Number(id));
        navigate('/tickets');
      } catch (error: any) {
        alert(error.response?.data?.detail || 'Failed to delete ticket');
      }
    }
  };

  const statusOptions = [
    { value: TicketStatus.CREATED, label: 'Created' },
    { value: TicketStatus.ASSIGNED, label: 'Assigned' },
    { value: TicketStatus.IN_PROGRESS, label: 'In Progress' },
    { value: TicketStatus.RESOLVED, label: 'Resolved' },
    { value: TicketStatus.CLOSED, label: 'Closed' },
  ];

  if (isLoading) {
    return (
      <DashboardLayout pageTitle={`Ticket #${id}`}>
        <div className="space-y-6 animate-pulse">
          <div className="h-10 bg-gray-200 rounded w-32"></div>
          <div className="h-8 bg-gray-200 rounded w-3/4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !ticket) {
    return (
      <DashboardLayout pageTitle={`Ticket #${id}`}>
        <div className="space-y-6">
          <Button variant="ghost" onClick={() => navigate('/tickets')}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Tickets
          </Button>
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
            {error || 'Ticket not found'}
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout pageTitle={`Ticket #${id}`}>
      <div className="space-y-6">
        {/* Back button */}
        <Button variant="ghost" onClick={() => navigate('/tickets')}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Tickets
        </Button>

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <StatusBadge status={ticket.status} />
              {ticket.priority && <PriorityBadge priority={ticket.priority} />}
            </div>
            <h2 className="text-2xl font-bold text-gray-900">{ticket.title}</h2>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => navigate(`/tickets/${id}/edit`)}>
              <Edit className="w-4 h-4 mr-2" />
              Edit
            </Button>
            <Button variant="danger" onClick={handleDelete}>
              <Trash2 className="w-4 h-4 mr-2" />
              Delete
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Description */}
            <Card>
              <CardHeader>
                <h2 className="text-lg font-semibold text-gray-900">Description</h2>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 whitespace-pre-wrap">{ticket.description}</p>
              </CardContent>
            </Card>

            {/* Comments Section (placeholder) */}
            <Card>
              <CardHeader>
                <h2 className="text-lg font-semibold text-gray-900">Comments</h2>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8 text-gray-500">
                  <p>No comments yet</p>
                  <p className="text-sm mt-2">Be the first to add a comment</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Status Update */}
            <Card>
              <CardHeader>
                <h3 className="font-semibold text-gray-900">Update Status</h3>
              </CardHeader>
              <CardContent>
                <Select
                  value={ticket.status}
                  onChange={(e) => handleStatusChange(e.target.value)}
                  options={statusOptions}
                  disabled={isUpdating}
                />
              </CardContent>
            </Card>

            {/* Ticket Details */}
            <Card>
              <CardHeader>
                <h3 className="font-semibold text-gray-900">Details</h3>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-start gap-3">
                  <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-700">Created</p>
                    <p className="text-sm text-gray-600">{formatDateTime(ticket.created_at)}</p>
                    <p className="text-xs text-gray-500">{formatRelativeTime(ticket.created_at)}</p>
                  </div>
                </div>

                {ticket.updated_at && (
                  <div className="flex items-start gap-3">
                    <Calendar className="w-5 h-5 text-gray-400 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-700">Last Updated</p>
                      <p className="text-sm text-gray-600">{formatDateTime(ticket.updated_at)}</p>
                      <p className="text-xs text-gray-500">{formatRelativeTime(ticket.updated_at)}</p>
                    </div>
                  </div>
                )}

                {ticket.created_by && (
                  <div className="flex items-start gap-3">
                    <User className="w-5 h-5 text-gray-400 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-700">Created By</p>
                      <p className="text-sm text-gray-600">User #{ticket.created_by}</p>
                    </div>
                  </div>
                )}

                {ticket.assigned_agent_id && (
                  <div className="flex items-start gap-3">
                    <User className="w-5 h-5 text-gray-400 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-700">Assigned To</p>
                      <p className="text-sm text-gray-600">Agent #{ticket.assigned_agent_id}</p>
                    </div>
                  </div>
                )}

                {ticket.category && (
                  <div className="flex items-start gap-3">
                    <Tag className="w-5 h-5 text-gray-400 mt-0.5" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-700">Category</p>
                      <p className="text-sm text-gray-600">{ticket.category}</p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

