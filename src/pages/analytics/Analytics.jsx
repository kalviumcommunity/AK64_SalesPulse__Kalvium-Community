import PageHeader from '@/components/layout/PageHeader'
import ChartCard from '@/components/charts/ChartCard'
import StatCard from '@/components/cards/StatCard'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, Legend } from 'recharts'
import { TrendingUp, Award, Percent } from 'lucide-react'

const revenueHistory = [
  { month: 'Jan', Sales: 42000, Target: 40000 },
  { month: 'Feb', Sales: 58000, Target: 45000 },
  { month: 'Mar', Sales: 62000, Target: 50000 },
  { month: 'Apr', Sales: 78000, Target: 55000 },
  { month: 'May', Sales: 80000, Target: 60000 },
  { month: 'Jun', Sales: 96000, Target: 65000 },
]

const stageEfficiency = [
  { name: 'Email', Conversion: 22, count: 240 },
  { name: 'Calls', Conversion: 34, count: 180 },
  { name: 'Demos', Conversion: 58, count: 95 },
  { name: 'Meetings', Conversion: 70, count: 42 },
]

function Analytics() {
  return (
    <div className="space-y-6">
      <PageHeader
        title="Analytics"
        description="Deep dive sales analytics, revenue trend analysis, and conversion efficiency metrics."
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <StatCard
          title="Conversion Rate"
          value="24.8%"
          icon={Percent}
          helper="+3.2% vs national average"
        />
        <StatCard
          title="Total Monthly Revenue"
          value="$96,000"
          icon={TrendingUp}
          helper="Jun target surpassed by 47%"
        />
        <StatCard
          title="Closed-Won Deals"
          // eslint-disable-next-line react/no-unstable-nested-components
          icon={() => <Award className="h-5 w-5" />}
          value="18"
          helper="Best performing sales month"
        />
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        <ChartCard
          title="Revenue Growth vs Target"
          description="A month-over-month comparison of active deal values closed against team targets."
        >
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={revenueHistory} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" stroke="#94a3b8" fontSize={12} />
                <YAxis stroke="#94a3b8" fontSize={12} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    borderColor: '#e2e8f0',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Legend verticalAlign="top" height={36} iconType="circle" fontSize={12} />
                <Line type="monotone" dataKey="Sales" stroke="#2563eb" strokeWidth={3} activeDot={{ r: 6 }} />
                <Line type="monotone" dataKey="Target" stroke="#94a3b8" strokeWidth={2} strokeDasharray="5 5" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>

        <ChartCard
          title="Conversion Efficiency by Channel"
          description="Average lead conversion percentage mapping the volume of client touches."
        >
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stageEfficiency} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
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
                <Bar dataKey="Conversion" fill="#3b82f6" radius={[4, 4, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </ChartCard>
      </div>
    </div>
  )
}

export default Analytics
