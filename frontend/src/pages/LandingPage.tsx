import { Link } from 'react-router-dom';
import { Ticket, CheckCircle, Zap, Users } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useCountAnimation } from '@/hooks/useCountAnimation';

export const LandingPage = () => {
  // Animated counters for stats with staggered delays
  const responseTime = useCountAnimation({ end: 50, duration: 1000, delay: 0 });
  const satisfaction = useCountAnimation({ end: 85, duration: 1000, delay: 150 });
  const ticketsResolved = useCountAnimation({ end: 10, duration: 1000, delay: 300 });

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-primary-100">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-primary-600 rounded-xl flex items-center justify-center">
                <Ticket className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold text-gray-900">TicketAI</span>
            </div>

            {/* Auth Buttons */}
            <div className="flex items-center gap-4">
              <Link to="/login">
                <Button variant="ghost">Login</Button>
              </Link>
              <Link to="/signup">
                <Button>Sign Up</Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            AI-Powered Support Ticket Management
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Streamline your customer support with intelligent ticket routing, 
            automated categorization, and real-time analytics.
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link to="/signup">
              <Button size="lg">Get Started Free</Button>
            </Link>
            <Link to="/login">
              <Button variant="outline" size="lg">View Demo</Button>
            </Link>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20">
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 text-center">
            <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Zap className="w-8 h-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              AI Auto-Categorization
            </h3>
            <p className="text-gray-600">
              Automatically categorize and prioritize tickets using AI-powered analysis
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 text-center">
            <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              Smart Workflow
            </h3>
            <p className="text-gray-600">
              Streamline your support process with automated routing and assignments
            </p>
          </div>

          <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-200 text-center">
            <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Users className="w-8 h-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">
              Team Collaboration
            </h3>
            <p className="text-gray-600">
              Enable seamless collaboration between support agents and managers
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20 text-center">
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">{responseTime}%</div>
            <div className="text-gray-600">Faster Response Time</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">{satisfaction}%</div>
            <div className="text-gray-600">Customer Satisfaction</div>
          </div>
          <div>
            <div className="text-4xl font-bold text-primary-600 mb-2">{ticketsResolved}K+</div>
            <div className="text-gray-600">Tickets Resolved</div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2026 TicketAI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

