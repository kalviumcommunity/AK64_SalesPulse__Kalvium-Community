import { useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell
} from 'recharts'
import { Users, DollarSign, TrendingUp, Star } from 'lucide-react'
import StatCard from '@/components/cards/StatCard'
import ChartCard from '@/components/charts/ChartCard'
import Card from '@/components/ui/Card'
import Badge from '@/components/ui/Badge'
import Table from '@/components/tables/Table'
import { useAuth } from '@/contexts/AuthContext'
import { Navigate } from 'react-router-dom'
import DateRangeFilter from '@/components/common/DateRangeFilter'

const quotaData = [
  { rep: 'Sarah J.',  attainment: 124 },
  { rep: 'Michael C.', attainment: 103 },
  { rep: 'Emma W.',  attainment: 88 },
  { rep: 'David M.', attainment: 71 },
  { rep: 'Clark K.', attainment: 95 },
  { rep: 'Diana P.', attainment: 116 },
]

const coachingQueue = [
  {
    rep: 'David Miller',
    note: 'Response time at 6.2h — 3 deals at risk of going cold. Recommend immediate 1:1.',
    tone: 'slate',
    tag: 'Urgent',
  },
  {
    rep: 'Emma Watson',
    note: 'Follow-up rate dropped 40% this month. Email sentiment trending negative.',
    tone: 'slate',
    tag: 'Flag',
  },
  {
    rep: 'Sarah Jenkins',
    note: 'Exceeding quota by 24%. Candidate for team mentorship programme this quarter.',
    tone: 'green',
    tag: 'Promote',
  },
]

const kpiData = [
  { id: 1, rep: 'Sarah Jenkins', deals: 12, revenue: '$144,000', respTime: '2.1h', behScore: '91', quota: '124%', status: 'Exceeding', tone: 'green' },
  { id: 2, rep: 'Diana Prince',  deals: 11, revenue: '$128,400', respTime: '2.6h', behScore: '85', quota: '116%', status: 'Exceeding', tone: 'green' },
  { id: 3, rep: 'Michael Chen',  deals: 9,  revenue: '$98,500',  respTime: '3.4h', behScore: '76', quota: '103%', status: 'On Track',  tone: 'blue' },
  { id: 4, rep: 'Clark Kent',    deals: 8,  revenue: '$87,200',  respTime: '3.1h', behScore: '79', quota: '95%',  status: 'On Track',  tone: 'blue' },
  { id: 5, rep: 'Emma Watson',   deals: 7,  revenue: '$76,200',  respTime: '4.8h', behScore: '59', quota: '88%',  status: 'At Risk',   tone: 'slate' },
  { id: 6, rep: 'David Miller',  deals: 5,  revenue: '$54,000',  respTime: '6.2h', behScore: '42', quota: '71%',  status: 'Critical',  tone: 'slate' },
]

const columns = [
  { key: 'rep',      header: 'Sales Rep' },
  { key: 'deals',    header: 'Deals Closed' },
  { key: 'revenue',  header: 'Revenue', className: 'font-semibold text-secondary' },
  { key: 'respTime', header: 'Avg Response' },
  { key: 'behScore', header: 'Behaviour Score' },
  { key: 'quota',    header: 'Quota Attainment' },
  {
    key: 'status',
    header: 'Status',
    render: (row) => <Badge tone={row.tone}>{row.status}</Badge>,
  },
]

const BAR_COLORS = quotaData.map((d) =>
  d.attainment >= 100 ? '#2563eb' : d.attainment >= 85 ? '#60a5fa' : '#f87171'
)

export default function Team() {
  const { user } = useAuth()
  const role = user?.role?.toLowerCase()

  const [dateRange, setDateRange] = useState('30d')

  if (role === 'representative') {
    return <Navigate to="/performance" replace />
  }

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-secondary">Team Performance</h1>
          <p className="mt-1 text-sm text-slate-500">
            Manager view: quota attainment rollup, coaching queue, and individual rep KPIs.
          </p>
        </div>
        <DateRangeFilter value={dateRange} onChange={setDateRange} />
      </div>

      {/* KPI Row */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Team Quota (MTD)"  value="$588K"  icon={DollarSign}  helper="Target: $600K" />
        <StatCard title="Team Attainment"   value="98%"    icon={TrendingUp}  helper="2pp below target" />
        <StatCard title="Active Reps"       value="6 / 8"  icon={Users}       helper="2 reps on leave" />
        <StatCard title="Team Health Score" value="74/100" icon={Star}        helper="↑ 6pts vs last month" />
      </div>

      {/* Chart + Coaching Queue */}
      <div className="grid gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <ChartCard title="Quota Attainment" description="Individual rep performance against this month's quota target.">
            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={quotaData} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="rep" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} domain={[0, 140]} tickFormatter={(v) => `${v}%`} />
                  <Tooltip
                    formatter={(v) => [`${v}%`, 'Attainment']}
                    contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#e2e8f0' }}
                  />
                  {/* 100% reference line via custom tick */}
                  <Bar dataKey="attainment" radius={[4, 4, 0, 0]} barSize={36}>
                    {quotaData.map((_, i) => (
                      <Cell key={i} fill={BAR_COLORS[i]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>

        <Card>
          <h2 className="mb-3 text-sm font-semibold text-secondary">Team Health Alerts</h2>
          <div className="space-y-3">
            {coachingQueue.map((item) => (
              <div key={item.rep} className="rounded-lg border border-border p-3">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <p className="text-xs font-semibold text-secondary">{item.rep}</p>
                  <Badge tone={item.tone}>{item.tag}</Badge>
                </div>
                <p className="text-xs text-slate-500">{item.note}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* KPI Table */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold text-secondary">Key Performance Indicators</h2>
        <Table columns={columns} data={kpiData} />
      </div>
    </div>
  )
}
