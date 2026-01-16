import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { Ticket as TicketIcon, CheckCircle, Clock, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { ticketsApi } from '@/api/tickets';
import { Ticket, TicketStatus } from '@/types';

export const DashboardPage = () => {
  const navigate = useNavigate();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        setIsLoading(true);
        const data = await ticketsApi.getAll();
        setTickets(data);
      } catch (error) {
        console.error('Failed to fetch tickets:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTickets();
  }, []);

  // Calculate stats from tickets
  const totalTickets = tickets.length;
  const openTickets = tickets.filter(t => 
    t.status === TicketStatus.CREATED || t.status === TicketStatus.ASSIGNED
  ).length;
  const inProgressTickets = tickets.filter(t => 
    t.status === TicketStatus.IN_PROGRESS
  ).length;
  const resolvedTickets = tickets.filter(t => 
    t.status === TicketStatus.RESOLVED || t.status === TicketStatus.CLOSED
  ).length;

  const stats = [
    {
      title: 'Total Tickets',
      value: totalTickets.toString(),
      change: '+12%',
      icon: TicketIcon,
      color: 'bg-blue-500',
    },
    {
      title: 'Open Tickets',
      value: openTickets.toString(),
      change: '+5%',
      icon: AlertCircle,
      color: 'bg-yellow-500',
    },
    {
      title: 'In Progress',
      value: inProgressTickets.toString(),
      change: '+8%',
      icon: Clock,
      color: 'bg-orange-500',
    },
    {
      title: 'Resolved',
      value: resolvedTickets.toString(),
      change: '+15%',
      icon: CheckCircle,
      color: 'bg-green-500',
    },
  ];

  // Get recent tickets (last 4)
  const recentTickets = tickets.slice(0, 4);

  return (
    <DashboardLayout pageTitle="Dashboard">
      <div className="space-y-6">
        {/* Header */}
        <div>
          <p className="text-gray-600">Overview of your support ticket system</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {isLoading ? (
            [...Array(4)].map((_, i) => (
              <Card key={i}>
                <CardContent className="pt-6">
                  <div className="animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                    <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-2/3"></div>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            stats.map((stat) => (
              <Card key={stat.title}>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                      <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
                      <p className="text-sm text-green-600 mt-1">{stat.change} from last week</p>
                    </div>
                    <div className={`w-12 h-12 ${stat.color} rounded-lg flex items-center justify-center`}>
                      <stat.icon className="w-6 h-6 text-white" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Recent Tickets */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Recent Tickets</h2>
              <button
                onClick={() => navigate('/tickets')}
                className="text-sm text-primary-600 hover:text-primary-700 font-medium"
              >
                View all
              </button>
            </div>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-4">
                {[...Array(4)].map((_, i) => (
                  <div key={i} className="p-4 bg-gray-50 rounded-lg animate-pulse">
                    <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                    <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                  </div>
                ))}
              </div>
            ) : recentTickets.length > 0 ? (
              <div className="space-y-4">
                {recentTickets.map((ticket) => (
                  <div
                    key={ticket.id}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
                    onClick={() => navigate(`/tickets/${ticket.id}`)}
                  >
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-sm font-medium text-gray-500">#{ticket.id}</span>
                        {ticket.priority && (
                          <span className={`text-xs px-2 py-0.5 rounded-full ${
                            ticket.priority === 'HIGH' ? 'bg-red-100 text-red-700' :
                            ticket.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
                            'bg-green-100 text-green-700'
                          }`}>
                            {ticket.priority}
                          </span>
                        )}
                      </div>
                      <p className="font-medium text-gray-900">{ticket.title}</p>
                    </div>
                    <span className={`text-xs px-3 py-1 rounded-full ${
                      ticket.status === TicketStatus.RESOLVED || ticket.status === TicketStatus.CLOSED ? 'bg-green-100 text-green-700' :
                      ticket.status === TicketStatus.IN_PROGRESS ? 'bg-yellow-100 text-yellow-700' :
                      ticket.status === TicketStatus.ASSIGNED ? 'bg-blue-100 text-blue-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {ticket.status.replace('_', ' ')}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <p>No tickets yet</p>
                <button
                  onClick={() => navigate('/tickets/new')}
                  className="mt-2 text-primary-600 hover:text-primary-700"
                >
                  Create your first ticket
                </button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

