import { useState } from 'react'
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend
} from 'recharts'
import { TrendingUp, Award, Clock, Users } from 'lucide-react'
import StatCard from '@/components/cards/StatCard'
import ChartCard from '@/components/charts/ChartCard'
import Card from '@/components/ui/Card'
import Badge from '@/components/ui/Badge'
import Table from '@/components/tables/Table'
import DateRangeFilter from '@/components/common/DateRangeFilter'

const revenueTrend = [
  { month: 'Jan', Sales: 42000, Target: 40000 },
  { month: 'Feb', Sales: 58000, Target: 45000 },
  { month: 'Mar', Sales: 62000, Target: 50000 },
  { month: 'Apr', Sales: 78000, Target: 55000 },
  { month: 'May', Sales: 80000, Target: 60000 },
  { month: 'Jun', Sales: 96000, Target: 65000 },
  { month: 'Jul', Sales: 89000, Target: 70000 },
]

const channelData = [
  { name: 'Email', value: 38 },
  { name: 'Phone', value: 27 },
  { name: 'Demo', value: 19 },
  { name: 'Meeting', value: 16 },
]

const insights = [
  { label: 'Sarah Jenkins', note: 'Closed 3 deals this week — 40% above personal best', tone: 'green', tag: 'Top Performer' },
  { label: 'David Miller', note: 'Response time at 6.2h — exceeds team avg of 3.4h', tone: 'slate', tag: 'Needs Attention' },
  { label: 'Enterprise Q3', note: '4 high-value deals at negotiation — review urgently', tone: 'blue', tag: 'Opportunity' },
]

const topPerformers = [
  { id: 1, rep: 'Sarah Jenkins', deals: 12, revenue: '$144,000', winRate: '72%', quota: '124%', status: 'Exceeding', tone: 'green' },
  { id: 2, rep: 'Michael Chen', deals: 9,  revenue: '$98,500',  winRate: '61%', quota: '103%', status: 'On Track',  tone: 'blue' },
  { id: 3, rep: 'Emma Watson',  deals: 7,  revenue: '$76,200',  winRate: '58%', quota: '88%',  status: 'At Risk',   tone: 'slate' },
  { id: 4, rep: 'David Miller', deals: 5,  revenue: '$54,000',  winRate: '44%', quota: '71%',  status: 'At Risk',   tone: 'slate' },
]

const columns = [
  { key: 'rep',     header: 'Sales Rep' },
  { key: 'deals',   header: 'Deals Closed' },
  { key: 'revenue', header: 'Revenue', className: 'font-semibold text-secondary' },
  { key: 'winRate', header: 'Win Rate' },
  { key: 'quota',   header: 'Quota Attainment' },
  {
    key: 'status',
    header: 'Status',
    render: (row) => <Badge tone={row.tone}>{row.status}</Badge>,
  },
]

export default function Performance() {
  const [dateRange, setDateRange] = useState('30d')

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-secondary">Performance</h1>
          <p className="mt-1 text-sm text-slate-500">Sales performance metrics and individual contribution overview.</p>
        </div>
        <DateRangeFilter value={dateRange} onChange={setDateRange} />
      </div>

      {/* KPI Row */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Today's Achievement" value="$12,400" icon={TrendingUp} helper="+18% vs yesterday" />
        <StatCard title="Win Rate (MTD)" value="63.2%" icon={Award} helper="Team avg: 54.1%" />
        <StatCard title="Avg Cycle Time" value="18 days" icon={Clock} helper="−2 days vs last month" />
        <StatCard title="Active Reps" value="8 / 10" icon={Users} helper="2 reps on leave" />
      </div>

      {/* Charts */}
      <div className="grid gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <ChartCard title="Revenue Trend" description="Monthly sales closed vs target across the team.">
            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={revenueTrend} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="perfSales" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#2563eb" stopOpacity={0.2} />
                      <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="month" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#e2e8f0' }} />
                  <Legend verticalAlign="top" height={32} iconType="circle" style={{ fontSize: '12px' }} />
                  <Area type="monotone" dataKey="Sales" stroke="#2563eb" strokeWidth={2.5} fill="url(#perfSales)" />
                  <Area type="monotone" dataKey="Target" stroke="#94a3b8" strokeWidth={2} strokeDasharray="5 5" fill="none" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>

        <ChartCard title="Activity by Channel" description="Share of customer touchpoints by type.">
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={channelData} margin={{ top: 8, right: 8, left: -28, bottom: 0 }} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
                <XAxis type="number" stroke="#94a3b8" fontSize={11} />
                <YAxis type="category" dataKey="name" stroke="#94a3b8" fontSize={11} width={52} />
                <Tooltip contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#e2e8f0' }} />
                <Bar dataKey="value" fill="#2563eb" radius={[0, 4, 4, 0]} barSize={16} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>

      {/* Performance Insights */}
      <div className="grid gap-4 xl:grid-cols-3">
        <Card>
          <h2 className="mb-3 text-sm font-semibold text-secondary">Performance Insights</h2>
          <div className="space-y-3">
            {insights.map((item) => (
              <div key={item.label} className="rounded-lg border border-border p-3">
                <div className="flex items-center justify-between mb-1">
                  <p className="text-sm font-semibold text-secondary">{item.label}</p>
                  <Badge tone={item.tone}>{item.tag}</Badge>
                </div>
                <p className="text-xs text-slate-500">{item.note}</p>
              </div>
            ))}
          </div>
        </Card>

        <div className="xl:col-span-2">
          <div className="space-y-3">
            <h2 className="text-sm font-semibold text-secondary">Top Performers</h2>
            <Table columns={columns} data={topPerformers} />
          </div>
        </div>
      </div>
    </div>
  )
}
