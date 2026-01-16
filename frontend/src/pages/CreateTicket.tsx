import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { Card, CardContent, CardHeader } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Textarea } from '@/components/ui/Textarea';
import { Button } from '@/components/ui/Button';
import { ArrowLeft } from 'lucide-react';
import { ticketsApi } from '@/api/tickets';

const ticketSchema = z.object({
  title: z.string().min(5, 'Title must be at least 5 characters').max(255, 'Title must be less than 255 characters'),
  description: z.string().min(20, 'Description must be at least 20 characters').max(2000, 'Description must be less than 2000 characters'),
});

type TicketFormData = z.infer<typeof ticketSchema>;

export const CreateTicketPage = () => {
  const navigate = useNavigate();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<TicketFormData>({
    resolver: zodResolver(ticketSchema),
  });

  const descriptionValue = watch('description', '');

  const onSubmit = async (data: TicketFormData) => {
    setIsSubmitting(true);
    setError('');

    try {
      // Call the create ticket API
      const newTicket = await ticketsApi.create(data);
      
      // Navigate to the new ticket detail page
      navigate(`/tickets/${newTicket.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create ticket');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <DashboardLayout pageTitle="Create New Ticket">
      <div className="max-w-3xl mx-auto space-y-6">
        {/* Back button */}
        <Button variant="ghost" onClick={() => navigate('/tickets')}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Tickets
        </Button>

        {/* Header */}
        <div>
          <p className="text-gray-600">Submit a new support ticket</p>
        </div>

        {/* Form */}
        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold text-gray-900">Ticket Details</h2>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {error && (
                <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600">
                  {error}
                </div>
              )}

              <Input
                label="Title"
                placeholder="Brief description of the issue"
                error={errors.title?.message}
                {...register('title')}
                required
              />

              <div>
                <Textarea
                  label="Description"
                  placeholder="Provide detailed information about the issue..."
                  rows={8}
                  error={errors.description?.message}
                  {...register('description')}
                  required
                />
                <div className="mt-1 text-sm text-gray-500 text-right">
                  {descriptionValue.length} / 2000 characters
                </div>
              </div>

              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h3 className="text-sm font-medium text-blue-900 mb-2">💡 Tips for a better ticket</h3>
                <ul className="text-sm text-blue-700 space-y-1 ml-4 list-disc">
                  <li>Be specific and provide as much detail as possible</li>
                  <li>Include error messages if applicable</li>
                  <li>Mention steps to reproduce the issue</li>
                  <li>Specify which browser/device you're using</li>
                </ul>
              </div>

              <div className="flex gap-4">
                <Button type="submit" isLoading={isSubmitting} className="flex-1">
                  {isSubmitting ? 'Creating...' : 'Create Ticket'}
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => navigate('/tickets')}
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        {/* Help Section */}
        <Card>
          <CardContent className="py-4">
            <p className="text-sm text-gray-600">
              Need immediate assistance? Contact our support team at{' '}
              <a href="mailto:support@example.com" className="text-primary-600 hover:text-primary-700 font-medium">
                support@example.com
              </a>
            </p>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
};

