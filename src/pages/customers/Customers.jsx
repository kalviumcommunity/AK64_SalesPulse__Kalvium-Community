import PageHeader from '@/components/layout/PageHeader'
import Table from '@/components/tables/Table'
import Badge from '@/components/ui/Badge'

const customersData = [
  {
    id: 1,
    name: 'Robert Downey',
    company: 'Stark Industries',
    email: 'robert@stark.com',
    sentiment: 'Positive',
    tone: 'green',
    tier: 'Enterprise',
    activity: '2 hours ago',
  },
  {
    id: 2,
    name: 'Bruce Wayne',
    company: 'Wayne Enterprises',
    email: 'bruce@wayne.com',
    sentiment: 'Critical',
    tone: 'slate',
    tier: 'Enterprise',
    activity: '1 day ago',
  },
  {
    id: 3,
    name: 'Peter Parker',
    company: 'Daily Bugle',
    email: 'peter@bugle.com',
    sentiment: 'Neutral',
    tone: 'blue',
    tier: 'Mid-Market',
    activity: '3 days ago',
  },
  {
    id: 4,
    name: 'Clark Kent',
    company: 'Daily Planet',
    email: 'clark@planet.com',
    sentiment: 'Positive',
    tone: 'green',
    tier: 'SMB',
    activity: '4 days ago',
  },
  {
    id: 5,
    name: 'Diana Prince',
    company: 'Themyscira Museum',
    email: 'diana@museum.org',
    sentiment: 'Positive',
    tone: 'green',
    tier: 'Enterprise',
    activity: 'Just now',
  },
]

const columns = [
  { key: 'name', header: 'Contact Name' },
  { key: 'company', header: 'Company' },
  { key: 'email', header: 'Email Address' },
  {
    key: 'sentiment',
    header: 'Sentiment Health',
    render: (row) => <Badge tone={row.tone}>{row.sentiment}</Badge>,
  },
  { key: 'tier', header: 'Account Tier' },
  { key: 'activity', header: 'Last Touchpoint', className: 'text-slate-500' },
]

function Customers() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Customers"
        description="Comprehensive customer intelligence, behavior health, and account tier details."
      />
      <div className="bg-white rounded-xl shadow-sm border border-slate-100 p-1">
        <Table columns={columns} data={customersData} />
      </div>
    </div>
  )
}

export default Customers
