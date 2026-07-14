import { Calendar } from 'lucide-react'
import { cn } from '@/utils/cn'

const RANGES = [
  { label: 'This Week',  value: '7d'  },
  { label: 'This Month', value: '30d' },
  { label: 'Last 3M',   value: '90d' },
  { label: 'YTD',       value: 'ytd' },
]

export default function DateRangeFilter({ value, onChange, className }) {
  return (
    <div className={cn('flex items-center gap-1.5', className)}>
      <Calendar className="h-4 w-4 text-slate-400 shrink-0" />
      <div className="flex rounded-lg border border-border overflow-hidden bg-white">
        {RANGES.map((r) => (
          <button
            key={r.value}
            type="button"
            onClick={() => onChange(r.value)}
            className={cn(
              'px-3 py-1.5 text-xs font-semibold transition cursor-pointer',
              value === r.value
                ? 'bg-primary text-white'
                : 'text-slate-600 hover:bg-slate-50'
            )}
          >
            {r.label}
          </button>
        ))}
      </div>
    </div>
  )
}
