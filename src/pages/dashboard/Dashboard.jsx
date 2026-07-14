import { Activity, BrainCircuit, Handshake, Users } from 'lucide-react'
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
  Cell,
} from 'recharts'
import ChartCard from '@/components/charts/ChartCard'
import PageHeader from '@/components/layout/PageHeader'
import StatCard from '@/components/cards/StatCard'
import Table from '@/components/tables/Table'
import Badge from '@/components/ui/Badge'

const trendData = [
  { name: 'Jan', 'Activity Level': 140, 'Sentiment Score': 68 },
  { name: 'Feb', 'Activity Level': 220, 'Sentiment Score': 72 },
  { name: 'Mar', 'Activity Level': 290, 'Sentiment Score': 70 },
  { name: 'Apr', 'Activity Level': 380, 'Sentiment Score': 80 },
  { name: 'May', 'Activity Level': 350, 'Sentiment Score': 78 },
  { name: 'Jun', 'Activity Level': 480, 'Sentiment Score': 85 },
]

const dealData = [
  { name: 'Discovery', value: 12 },
  { name: 'Qualification', value: 15 },
  { name: 'Proposal', value: 9 },
  { name: 'Negotiation', value: 6 },
  { name: 'Closing', value: 3 },
]

const COLORS = ['#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe']

const recentInteractions = [
  {
    id: 1,
    customer: 'Acme Corp',
    rep: 'Sarah Jenkins',
    method: 'Video Call',
    sentiment: 'Positive',
    tone: 'green',
    status: 'High Interest',
    date: 'Today, 10:14 AM',
  },
  {
    id: 2,
    customer: 'GlobalTech Ltd',
    rep: 'Michael Chen',
    method: 'Email',
    sentiment: 'Neutral',
    tone: 'blue',
    status: 'Follow-up Scheduled',
    date: 'Yesterday, 4:30 PM',
  },
  {
    id: 3,
    customer: 'Stark Industries',
    rep: 'David Miller',
    method: 'In-person Meeting',
    sentiment: 'Positive',
    tone: 'green',
    status: 'Proposal Submitted',
    date: 'Jul 13, 2026',
  },
  {
    id: 4,
    customer: 'Wayne Enterprises',
    rep: 'Emma Watson',
    method: 'Phone Call',
    sentiment: 'Critical',
    tone: 'slate',
    status: 'Churn Alert',
    date: 'Jul 12, 2026',
  },
]

const columns = [
  { key: 'customer', header: 'Customer' },
  { key: 'rep', header: 'Sales Representative' },
  { key: 'method', header: 'Interaction Type' },
  {
    key: 'sentiment',
    header: 'Sentiment',
    render: (row) => <Badge tone={row.tone}>{row.sentiment}</Badge>,
  },
  { key: 'status', header: 'Status' },
  { key: 'date', header: 'Date', className: 'text-slate-500' },
]

function Dashboard() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="Executive sales behaviour intelligence and performance overview dashboard."
      />

      {/* Stats Cards */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard
          title="Total Customers"
          value="1,248"
          icon={Users}
          helper="+12% growth this month"
        />
        <StatCard
          title="Open Deals"
          value="45"
          icon={Handshake}
          helper="Pipeline value: $620k"
        />
        <StatCard
          title="Activities Logged"
          value="384"
          icon={Activity}
          helper="This week across all channels"
        />
        <StatCard
          title="AI Signals"
          value="12"
          icon={BrainCircuit}
          helper="8 urgent recommendations"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid gap-4 xl:grid-cols-2">
        <ChartCard
          title="Sales Behaviour & Activity Trend"
          description="Monthly volume of client interactions mapped against average team sentiment."
        >
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorActivity" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563eb" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    borderColor: '#e2e8f0',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="Activity Level"
                  stroke="#2563eb"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#colorActivity)"
                />
                <Area
                  type="monotone"
                  dataKey="Sentiment Score"
                  stroke="#10b981"
                  strokeWidth={2}
                  fill="none"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard
          title="Deal Health Distribution"
          description="Total number of deals currently active in each sales pipeline stage."
        >
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dealData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    borderColor: '#e2e8f0',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {dealData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Table Section */}
      <div className="space-y-3">
        <h2 className="text-lg font-semibold text-secondary">Recent Customer Interactions</h2>
        <Table columns={columns} data={recentInteractions} />
      </div>
    </div>
  )
}

export default Dashboard
