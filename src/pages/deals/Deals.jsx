import PageHeader from '@/components/layout/PageHeader'
import Table from '@/components/tables/Table'
import Badge from '@/components/ui/Badge'

const dealsData = [
  {
    id: 1,
    name: 'Enterprise Cloud Suite License',
    account: 'Stark Industries',
    value: '$120,000',
    stage: 'Proposal',
    health: 'Strong',
    tone: 'green',
    nextAction: 'Finalize Pricing Agreement',
  },
  {
    id: 2,
    name: 'Hardware Fleet Renewal',
    account: 'Wayne Enterprises',
    value: '$245,000',
    stage: 'Negotiation',
    health: 'Critical',
    tone: 'slate',
    nextAction: 'Review Compliance terms',
  },
  {
    id: 3,
    name: 'API Support Integration SLA',
    account: 'GlobalTech Ltd',
    value: '$35,000',
    stage: 'Discovery',
    health: 'Neutral',
    tone: 'blue',
    nextAction: 'Schedule Demo session',
  },
  {
    id: 4,
    name: 'SaaS Analytics Expansion',
    account: 'Acme Corp',
    value: '$48,000',
    stage: 'Closing',
    health: 'Strong',
    tone: 'green',
    nextAction: 'Collect Signature',
  },
  {
    id: 5,
    name: 'Advertising Platform Placement',
    account: 'Daily Bugle',
    value: '$12,000',
    stage: 'Qualification',
    health: 'Neutral',
    tone: 'blue',
    nextAction: 'Arrange Meeting with Editor',
  },
]

const columns = [
  { key: 'name', header: 'Deal Name' },
  { key: 'account', header: 'Company' },
  { key: 'value', header: 'Deal Value', className: 'font-semibold text-secondary' },
  { key: 'stage', header: 'Pipeline Stage' },
  {
    key: 'health',
    header: 'Deal Health',
    render: (row) => <Badge tone={row.tone}>{row.health}</Badge>,
  },
  { key: 'nextAction', header: 'Next Action Step', className: 'text-slate-500' },
]

function Deals() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Deals"
        description="Deal pipeline status tracker, stages progress, and health indicator view."
      />
      <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-1">
        <Table columns={columns} data={dealsData} />
      </div>
    </div>
  )
}

export default Deals
