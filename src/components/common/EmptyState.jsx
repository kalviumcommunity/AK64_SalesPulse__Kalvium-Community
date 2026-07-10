import { Inbox } from 'lucide-react'
import Card from '@/components/ui/Card'

function EmptyState({ title = 'No data yet', description = 'Records will appear here once connected.' }) {
  return (
    <Card className="flex flex-col items-center justify-center py-12 text-center">
      <div className="rounded-xl bg-blue-50 p-3 text-primary">
        <Inbox className="h-6 w-6" />
      </div>
      <h2 className="mt-4 text-base font-semibold text-secondary">{title}</h2>
      <p className="mt-2 max-w-md text-sm text-slate-500">{description}</p>
    </Card>
  )
}

export default EmptyState
