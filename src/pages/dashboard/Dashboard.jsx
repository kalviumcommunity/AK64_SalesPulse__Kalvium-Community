import { Activity, BrainCircuit, Handshake, Users } from 'lucide-react'
import ChartCard from '@/components/charts/ChartCard'
import PageHeader from '@/components/layout/PageHeader'
import StatCard from '@/components/cards/StatCard'

function Dashboard() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Dashboard"
        description="Executive sales behaviour intelligence overview placeholder."
      />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Customers" value="--" icon={Users} helper="Ready for CRM data" />
        <StatCard title="Open Deals" value="--" icon={Handshake} helper="Ready for pipeline data" />
        <StatCard title="Activities" value="--" icon={Activity} helper="Ready for activity data" />
        <StatCard title="AI Signals" value="--" icon={BrainCircuit} helper="Ready for recommendations" />
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <ChartCard title="Sales Behaviour Trend" description="Recharts integration placeholder." />
        <ChartCard title="Deal Health Distribution" description="Analytics module placeholder." />
      </div>
    </div>
  )
}

export default Dashboard
