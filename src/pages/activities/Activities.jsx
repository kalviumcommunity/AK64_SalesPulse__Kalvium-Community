import PageHeader from '@/components/layout/PageHeader'
import Table from '@/components/tables/Table'
import Badge from '@/components/ui/Badge'

const activitiesData = [
  {
    id: 1,
    type: 'Outbound Email',
    tone: 'blue',
    customer: 'Acme Corp',
    rep: 'Sarah Jenkins',
    notes: 'Sent pricing follow-up email regarding custom integrations.',
    time: '10 mins ago',
  },
  {
    id: 2,
    type: 'Video Demo',
    tone: 'green',
    customer: 'GlobalTech Ltd',
    rep: 'Michael Chen',
    notes: 'Conducted platform walkthrough session covering behaviour tracking.',
    time: '2 hours ago',
  },
  {
    id: 3,
    type: 'In-Person Lunch',
    tone: 'green',
    customer: 'Stark Industries',
    rep: 'David Miller',
    notes: 'Met with Robert Downey to talk about enterprise licensing models.',
    time: '1 day ago',
  },
  {
    id: 4,
    type: 'Support Escalation',
    tone: 'slate',
    customer: 'Wayne Enterprises',
    notes: 'Logged complaint regarding account provisioning delays.',
    rep: 'Emma Watson',
    time: '2 days ago',
  },
  {
    id: 5,
    type: 'Discovery Call',
    tone: 'blue',
    customer: 'Daily Planet',
    rep: 'Clark Kent',
    notes: 'Exploratory call regarding news syndication analytics.',
    time: '3 days ago',
  },
]

const columns = [
  {
    key: 'type',
    header: 'Activity Type',
    render: (row) => <Badge tone={row.tone}>{row.type}</Badge>,
  },
  { key: 'customer', header: 'Customer' },
  { key: 'rep', header: 'Logged By' },
  { key: 'notes', header: 'Notes/Outcome', className: 'text-slate-600 max-w-xs truncate' },
  { key: 'time', header: 'Time Elapsed', className: 'text-slate-500' },
]

function Activities() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Activities"
        description="Comprehensive log of sales communications, meeting outlines, and activities history."
      />
      <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-1">
        <Table columns={columns} data={activitiesData} />
      </div>
    </div>
  )
}

export default Activities
