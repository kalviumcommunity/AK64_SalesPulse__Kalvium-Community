import { useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, FunnelChart, Funnel, LabelList
} from 'recharts'
import { DollarSign, TrendingUp, Percent, Target } from 'lucide-react'
import StatCard from '@/components/cards/StatCard'
import ChartCard from '@/components/charts/ChartCard'
import Card from '@/components/ui/Card'
import Badge from '@/components/ui/Badge'
import Table from '@/components/tables/Table'
import DateRangeFilter from '@/components/common/DateRangeFilter'

const stageData = [
  { stage: 'Prospect',      count: 24, value: 480000 },
  { stage: 'Qualification', count: 18, value: 360000 },
  { stage: 'Proposal',      count: 11, value: 220000 },
  { stage: 'Negotiation',   count: 7,  value: 140000 },
  { stage: 'Closing',       count: 4,  value:  80000 },
]

const alerts = [
  { deal: 'Stark Industries — Cloud Suite', note: 'No activity for 12 days', tone: 'slate', tag: 'Stalled' },
  { deal: 'Wayne Enterprises — Renewal',   note: 'Competitor proposal received', tone: 'slate', tag: 'At Risk' },
  { deal: 'Acme Corp — Expansion',         note: 'Decision expected in 3 days', tone: 'green', tag: 'Hot' },
]

const deals = [
  { id: 1, name: 'Cloud Suite License',   account: 'Stark Industries',  stage: 'Proposal',    prob: '68%', value: '$120,000', next: 'Finalize pricing agreement', tone: 'green', probTone: 'green' },
  { id: 2, name: 'Hardware Fleet Renewal', account: 'Wayne Enterprises', stage: 'Negotiation', prob: '42%', value: '$245,000', next: 'Review compliance terms',    tone: 'slate', probTone: 'slate' },
  { id: 3, name: 'API Support SLA',        account: 'GlobalTech Ltd',    stage: 'Discovery',   prob: '28%', value: '$35,000',  next: 'Schedule demo',             tone: 'blue',  probTone: 'blue'  },
  { id: 4, name: 'SaaS Analytics Package', account: 'Acme Corp',         stage: 'Closing',     prob: '89%', value: '$48,000',  next: 'Collect signature',         tone: 'green', probTone: 'green' },
  { id: 5, name: 'Ad Platform Deal',       account: 'Daily Bugle',       stage: 'Qualification', prob: '34%', value: '$12,000', next: 'Arrange meeting',          tone: 'blue',  probTone: 'blue'  },
]

const columns = [
  { key: 'name',    header: 'Deal Name' },
  { key: 'account', header: 'Account' },
  { key: 'stage',   header: 'Stage' },
  { key: 'value',   header: 'Value', className: 'font-semibold text-secondary' },
  {
    key: 'prob',
    header: 'Close Prob.',
    render: (row) => <Badge tone={row.probTone}>{row.prob}</Badge>,
  },
  { key: 'next', header: 'Next Action', className: 'text-slate-500 text-xs' },
]

export default function Pipeline() {
  const [dateRange, setDateRange] = useState('30d')

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-secondary">Pipeline Analytics</h1>
          <p className="mt-1 text-sm text-slate-500">Open deal visibility, stage distribution, and forecast metrics.</p>
        </div>
        <DateRangeFilter value={dateRange} onChange={setDateRange} />
      </div>

      {/* KPI Row */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Total Pipeline" value="$1.28M" icon={DollarSign} helper="64 active deals" />
        <StatCard title="Weighted Forecast" value="$484K" icon={TrendingUp} helper="Probability-adjusted value" />
        <StatCard title="Avg Close Prob." value="52%" icon={Percent} helper="↑ 4pp vs last quarter" />
        <StatCard title="Avg Deal Size" value="$20K" icon={Target} helper="Range: $8K – $245K" />
      </div>

      {/* Charts + Alerts */}
      <div className="grid gap-4 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <ChartCard title="Stage Breakdown" description="Deal count and cumulative value per pipeline stage.">
            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stageData} margin={{ top: 8, right: 8, left: -20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                  <XAxis dataKey="stage" stroke="#94a3b8" fontSize={11} />
                  <YAxis stroke="#94a3b8" fontSize={11} />
                  <Tooltip contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#e2e8f0' }} />
                  <Bar dataKey="count" name="Deals" fill="#2563eb" radius={[4, 4, 0, 0]} barSize={32} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </ChartCard>
        </div>

        <Card>
          <h2 className="mb-3 text-sm font-semibold text-secondary">Pipeline Alerts</h2>
          <div className="space-y-3">
            {alerts.map((a) => (
              <div key={a.deal} className="rounded-lg border border-border p-3">
                <div className="flex items-start justify-between gap-2 mb-1">
                  <p className="text-xs font-semibold text-secondary leading-snug">{a.deal}</p>
                  <Badge tone={a.tone}>{a.tag}</Badge>
                </div>
                <p className="text-xs text-slate-500">{a.note}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Deals Table */}
      <div className="space-y-3">
        <h2 className="text-sm font-semibold text-secondary">Major Open Deals</h2>
        <Table columns={columns} data={deals} />
      </div>
    </div>
  )
}
