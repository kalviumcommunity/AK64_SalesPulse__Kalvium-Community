import Card from '@/components/ui/Card'

function ChartCard({ title, description, children }) {
  return (
    <Card>
      <div className="mb-5">
        <h2 className="text-base font-semibold text-secondary">{title}</h2>
        {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
      </div>
      <div className="min-h-64 rounded-xl border border-dashed border-border bg-slate-50 p-4">
        {children || (
          <div className="flex h-56 items-center justify-center text-sm font-medium text-slate-500">
            Chart placeholder
          </div>
        )}
      </div>
    </Card>
  )
}

export default ChartCard
