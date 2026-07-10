import Card from '@/components/ui/Card'

function StatCard({ title, value, icon: Icon, helper }) {
  return (
    <Card>
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-3 text-2xl font-bold text-secondary">{value}</p>
          {helper && <p className="mt-2 text-xs text-slate-500">{helper}</p>}
        </div>
        {Icon && (
          <div className="rounded-xl bg-blue-50 p-3 text-primary">
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
    </Card>
  )
}

export default StatCard
