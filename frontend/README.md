# Support Ticket Frontend

Modern React + TypeScript frontend for the AI-Powered Support Ticket Analysis System.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at http://localhost:5173

## 📁 Project Structure

```
src/
├── api/              # API client and endpoint functions
│   ├── client.ts     # Axios configuration
│   ├── auth.ts       # Authentication APIs
│   ├── tickets.ts    # Ticket APIs
│   └── dashboard.ts  # Dashboard APIs
├── components/
│   ├── ui/           # Reusable UI components
│   ├── layout/       # Layout components (Sidebar, TopNav)
│   ├── tickets/      # Ticket-specific components
│   └── forms/        # Form components
├── pages/            # Page components
│   ├── Login.tsx
│   ├── Signup.tsx
│   ├── Dashboard.tsx
│   ├── TicketList.tsx
│   ├── TicketDetail.tsx
│   └── CreateTicket.tsx
├── store/            # Zustand state management
├── types/            # TypeScript type definitions
├── utils/            # Utility functions
├── App.tsx           # Main app component
└── main.tsx          # Entry point
```

## 🎨 Features

### ✅ Implemented
- Modern, responsive UI with Tailwind CSS
- Authentication pages (Login/Signup)
- Dashboard with statistics
- Ticket listing with filters and search
- Ticket detail view
- Create new ticket form
- Status management
- Role-based UI elements

### 🔄 Ready for API Integration
All API functions are defined and ready to be connected:
- Authentication (`authApi.login`, `authApi.register`)
- Tickets CRUD (`ticketsApi.getAll`, `ticketsApi.create`, etc.)
- Dashboard stats (`dashboardApi.getStats`)

Simply uncomment the TODO lines in the page components to enable API calls.

## 🛠️ Technologies

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router v6** - Routing
- **Zustand** - State management
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Axios** - HTTP client
- **Lucide React** - Icons
- **date-fns** - Date formatting

## 📝 Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## 🔗 API Integration

### Connect to Backend

1. Update `.env` file:
```env
VITE_API_URL=http://localhost:8000
```

2. Uncomment API calls in page components:
   - `src/pages/Login.tsx` - Line with `authApi.login`
   - `src/pages/TicketList.tsx` - Line with `ticketsApi.getAll`
   - etc.

3. Enable authentication guards in `App.tsx`

### API Functions Available

**Authentication:**
- `authApi.login(credentials)` - User login
- `authApi.register(data)` - User registration
- `authApi.getCurrentUser()` - Get current user

**Tickets:**
- `ticketsApi.getAll(params)` - List tickets
- `ticketsApi.getById(id)` - Get ticket details
- `ticketsApi.create(data)` - Create ticket
- `ticketsApi.update(id, data)` - Update ticket
- `ticketsApi.updateStatus(id, status)` - Update status
- `ticketsApi.delete(id)` - Delete ticket

**Dashboard:**
- `dashboardApi.getStats()` - Get dashboard statistics
- `dashboardApi.getTicketTrends()` - Get ticket trends
- `dashboardApi.getAgentPerformance()` - Get agent metrics

## 🎨 UI Components

### Basic Components
- `Button` - Primary, secondary, outline variants
- `Input` - Text input with validation
- `Textarea` - Multi-line text input
- `Select` - Dropdown select
- `Card` - Container component
- `Badge` - Status/priority badges

### Domain Components
- `StatusBadge` - Ticket status badge
- `PriorityBadge` - Ticket priority badge
- `TicketCard` - Ticket display card
- `Sidebar` - Navigation sidebar
- `TopNav` - Top navigation bar
- `DashboardLayout` - Main layout wrapper

## 🔐 Authentication

The app uses JWT token-based authentication:
- Tokens stored in localStorage
- Axios interceptor adds token to requests
- Auto-redirect on 401 errors
- Protected routes with auth guards

## 📱 Responsive Design

- Mobile-first approach
- Responsive sidebar (collapses on mobile)
- Adaptive layouts for all screen sizes
- Touch-friendly UI elements

## 🎯 Next Steps

1. **Install dependencies**: `npm install`
2. **Start dev server**: `npm run dev`
3. **Test the UI**: Navigate through all pages
4. **Connect to backend**: Update API calls when ready
5. **Customize**: Adjust colors, styles as needed

## 🤝 Contributing

When adding new features:
1. Follow existing code structure
2. Use TypeScript for type safety
3. Keep components small and reusable
4. Add proper error handling
5. Test responsiveness

## 📄 License

This project is part of the AI-Powered Support Ticket Analysis System.

---

**Happy Coding! 🚀**

