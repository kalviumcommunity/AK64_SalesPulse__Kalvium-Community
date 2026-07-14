import { useState } from 'react'
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend
} from 'recharts'
import { CheckCircle, XCircle, Percent, TrendingDown } from 'lucide-react'
import StatCard from '@/components/cards/StatCard'
import ChartCard from '@/components/charts/ChartCard'
import Card from '@/components/ui/Card'
import Badge from '@/components/ui/Badge'
import Table from '@/components/tables/Table'
import DateRangeFilter from '@/components/common/DateRangeFilter'

const winRateTrend = [
  { month: 'Jan', 'Win Rate': 48, 'Team Avg': 52 },
  { month: 'Feb', 'Win Rate': 53, 'Team Avg': 52 },
  { month: 'Mar', 'Win Rate': 59, 'Team Avg': 54 },
  { month: 'Apr', 'Win Rate': 55, 'Team Avg': 54 },
  { month: 'May', 'Win Rate': 63, 'Team Avg': 56 },
  { month: 'Jun', 'Win Rate': 68, 'Team Avg': 58 },
]

const lossReasons = [
  { reason: 'Price',       count: 14 },
  { reason: 'Competitor',  count: 10 },
  { reason: 'No Budget',   count: 8 },
  { reason: 'Timing',      count: 6 },
  { reason: 'Fit',         count: 4 },
]

const analysisInsights = [
  { label: 'Enterprise Wins', note: '3 of 4 enterprise proposals accepted — retain same pitch structure', tone: 'green', tag: 'Win Pattern' },
  { label: 'Price Sensitivity', note: 'Price objections account for 38% of losses — review discount policy', tone: 'slate', tag: 'Loss Driver' },
  { label: 'Q3 Opportunity', note: '6 stalled deals in Negotiation ready to re-engage with an updated offer', tone: 'blue', tag: 'Re-engage' },
]

const recentOutcomes = [
  { id: 1, deal: 'Cloud Suite License',    account: 'Stark Industries',   outcome: 'Won',  value: '$120,000', closeDate: 'Jul 10, 2026', rep: 'Sarah Jenkins', tone: 'green' },
  { id: 2, deal: 'Legacy Migration',       account: 'Oscorp',             outcome: 'Lost', value: '$85,000',  closeDate: 'Jul 8, 2026',  rep: 'David Miller',  tone: 'slate' },
  { id: 3, deal: 'SaaS Analytics Package', account: 'Acme Corp',          outcome: 'Won',  value: '$48,000',  closeDate: 'Jul 5, 2026',  rep: 'Michael Chen',  tone: 'green' },
  { id: 4, deal: 'Hardware Fleet',         account: 'LexCorp',            outcome: 'Lost', value: '$210,000', closeDate: 'Jun 29, 2026', rep: 'Emma Watson',   tone: 'slate' },
  { id: 5, deal: 'Ad Platform Placement',  account: 'Daily Planet',       outcome: 'Won',  value: '$18,000',  closeDate: 'Jun 25, 2026', rep: 'Clark Kent',    tone: 'green' },
]

const columns = [
  { key: 'deal',      header: 'Deal Name' },
  { key: 'account',   header: 'Account' },
  {
    key: 'outcome',
    header: 'Outcome',
    render: (row) => <Badge tone={row.tone}>{row.outcome}</Badge>,
  },
  { key: 'value',     header: 'Value', className: 'font-semibold text-secondary' },
  { key: 'rep',       header: 'Sales Rep' },
  { key: 'closeDate', header: 'Close Date', className: 'text-slate-500' },
]

export default function WinLoss() {
  const [dateRange, setDateRange] = useState('30d')

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-secondary">Win/Loss Analysis</h1>
          <p className="mt-1 text-sm text-slate-500">Historical deal outcomes, win rate trends, and key loss driver analysis.</p>
        </div>
        <DateRangeFilter value={dateRange} onChange={setDateRange} />
      </div>

      {/* KPI Row */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Win Rate (YTD)" value="63.8%" icon={Percent} helper="+7.2pp vs prior year" />
        <StatCard title="Total Closed" value="86" icon={TrendingDown} helper="Closed deals this year" />
        <StatCard title="Closed Won" value="55" icon={CheckCircle} helper="$1.04M total revenue" />
        <StatCard title="Closed Lost" value="31" icon={XCircle} helper="Avg loss value: $74K" />
      </div>

      {/* Charts + Insights */}
      <div className="grid gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2 space-y-4">
          <ChartCard title="Win Rate Trend" description="Monthly win rate versus team average benchmark.">
            <div className="h-52 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={winRateTrend} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="month" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#e2e8f0' }} />
                  <Legend verticalAlign="top" height={32} iconType="circle" style={{ fontSize: '12px' }} />
                  <Line type="monotone" dataKey="Win Rate" stroke="#2563eb" strokeWidth={2.5} dot={{ r: 3 }} />
                  <Line type="monotone" dataKey="Team Avg" stroke="#94a3b8" strokeWidth={2} strokeDasharray="5 5" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>

          <ChartCard title="Loss Reasons" description="Top reasons deals were marked as Closed Lost.">
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={lossReasons} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="reason" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#e2e8f0' }} />
                  <Bar dataKey="count" name="Count" fill="#f87171" radius={[4, 4, 0, 0]} barSize={36} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>

        <Card>
          <h2 className="mb-3 text-sm font-semibold text-secondary">Analysis Priority</h2>
          <div className="space-y-3">
            {analysisInsights.map((item) => (
              <div key={item.label} className="rounded-lg border border-border p-3">
                <div className="flex items-center justify-between gap-2 mb-1">
                  <p className="text-xs font-semibold text-secondary">{item.label}</p>
                  <Badge tone={item.tone}>{item.tag}</Badge>
                </div>
                <p className="text-xs text-slate-500">{item.note}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Recent Outcomes Table */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold text-secondary">Recent Outcomes</h2>
        <Table columns={columns} data={recentOutcomes} />
      </div>
    </div>
  )
}
