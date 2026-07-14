import { useState } from 'react'
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend
} from 'recharts'
import { Clock, Repeat, MessageSquare, Star } from 'lucide-react'
import StatCard from '@/components/cards/StatCard'
import ChartCard from '@/components/charts/ChartCard'
import Card from '@/components/ui/Card'
import Badge from '@/components/ui/Badge'
import Table from '@/components/tables/Table'
import DateRangeFilter from '@/components/common/DateRangeFilter'

const followUpTrend = [
  { week: 'W1', Frequency: 2.1, Benchmark: 3.0 },
  { week: 'W2', Frequency: 2.4, Benchmark: 3.0 },
  { week: 'W3', Frequency: 2.9, Benchmark: 3.0 },
  { week: 'W4', Frequency: 3.2, Benchmark: 3.0 },
  { week: 'W5', Frequency: 3.5, Benchmark: 3.0 },
  { week: 'W6', Frequency: 3.1, Benchmark: 3.0 },
]

const activityMix = [
  { rep: 'Sarah J.', Calls: 28, Emails: 42, Meetings: 12 },
  { rep: 'Michael C.', Calls: 20, Emails: 38, Meetings: 9 },
  { rep: 'Emma W.', Calls: 16, Emails: 29, Meetings: 7 },
  { rep: 'David M.', Calls: 12, Emails: 24, Meetings: 4 },
]

const behaviourAlerts = [
  {
    rep: 'David Miller',
    note: 'Avg response time 6.2h — exceeds 4h benchmark on 3 open deals',
    tone: 'slate',
    tag: 'Late Response',
  },
  {
    rep: 'Emma Watson',
    note: 'Follow-up frequency dropped 40% vs prior month — flagged for coaching',
    tone: 'slate',
    tag: 'Low Engagement',
  },
  {
    rep: 'Sarah Jenkins',
    note: 'Tone score 87/100 — highest on team, positive email sentiment trending up',
    tone: 'green',
    tag: 'Top Behaviour',
  },
]

const scorecard = [
  { id: 1, rep: 'Sarah Jenkins', respTime: '2.1h', followUps: 3.8, toneScore: '87',  behScore: '91', status: 'Excellent', tone: 'green' },
  { id: 2, rep: 'Michael Chen',  respTime: '3.4h', followUps: 3.1, toneScore: '74',  behScore: '76', status: 'Good',      tone: 'blue' },
  { id: 3, rep: 'Emma Watson',   respTime: '4.8h', followUps: 2.2, toneScore: '68',  behScore: '59', status: 'At Risk',   tone: 'slate' },
  { id: 4, rep: 'David Miller',  respTime: '6.2h', followUps: 1.9, toneScore: '54',  behScore: '42', status: 'Critical',  tone: 'slate' },
]

const columns = [
  { key: 'rep',       header: 'Sales Rep' },
  { key: 'respTime',  header: 'Avg Response Time' },
  { key: 'followUps', header: 'Follow-ups / wk' },
  { key: 'toneScore', header: 'Tone Score' },
  { key: 'behScore',  header: 'Behaviour Score', className: 'font-semibold text-secondary' },
  {
    key: 'status',
    header: 'Status',
    render: (row) => <Badge tone={row.tone}>{row.status}</Badge>,
  },
]

export default function Behaviour() {
  const [dateRange, setDateRange] = useState('30d')

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-secondary">Behaviour Analytics</h1>
          <p className="mt-1 text-sm text-slate-500">
            AI-derived behavioural metrics: response times, follow-up frequency, and tone intelligence.
          </p>
        </div>
        <DateRangeFilter value={dateRange} onChange={setDateRange} />
      </div>

      {/* KPI Row */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Avg Response Time" value="3.8h"  icon={Clock}        helper="Team benchmark: 3.0h" />
        <StatCard title="Follow-up / Week"  value="2.9x"  icon={Repeat}       helper="↑ 0.4x vs last month" />
        <StatCard title="Avg Tone Score"    value="71/100" icon={MessageSquare} helper="Positive emails: 62%" />
        <StatCard title="Behaviour Score"   value="67/100" icon={Star}          helper="Composite AI metric" />
      </div>

      {/* Charts + Alerts */}
      <div className="grid gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2 space-y-4">
          <ChartCard
            title="Follow-up Frequency Trend"
            description="Weekly average follow-up interactions vs the team benchmark."
          >
            <div className="h-52 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={followUpTrend} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="week" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#e2e8f0' }} />
                  <Legend verticalAlign="top" height={32} iconType="circle" style={{ fontSize: '12px' }} />
                  <Line type="monotone" dataKey="Frequency"  stroke="#2563eb" strokeWidth={2.5} dot={{ r: 3 }} />
                  <Line type="monotone" dataKey="Benchmark" stroke="#94a3b8" strokeWidth={2} strokeDasharray="5 5" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>

          <ChartCard title="Activity Mix by Rep" description="Breakdown of calls, emails, and meetings per representative.">
            <div className="h-48 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={activityMix} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="rep" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#e2e8f0' }} />
                  <Legend verticalAlign="top" height={32} iconType="circle" style={{ fontSize: '12px' }} />
                  <Bar dataKey="Calls"    stackId="a" fill="#2563eb" radius={[0, 0, 0, 0]} />
                  <Bar dataKey="Emails"   stackId="a" fill="#60a5fa" radius={[0, 0, 0, 0]} />
                  <Bar dataKey="Meetings" stackId="a" fill="#bfdbfe" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>

        <Card>
          <h2 className="mb-3 text-sm font-semibold text-secondary">Behaviour Intelligence</h2>
          <div className="space-y-3">
            {behaviourAlerts.map((item) => (
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

      {/* Behaviour Scorecard Table */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold text-secondary">Behaviour Scorecard</h2>
        <Table columns={columns} data={scorecard} />
      </div>
    </div>
  )
}
