import { cn } from '@/utils/cn'

const tones = {
  blue: 'bg-blue-50 text-primary ring-blue-100',
  slate: 'bg-slate-100 text-slate-700 ring-slate-200',
  green: 'bg-emerald-50 text-emerald-700 ring-emerald-100',
}

function Badge({ children, tone = 'blue', className }) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold ring-1',
        tones[tone],
        className,
      )}
    >
      {children}
    </span>
  )
}

export default Badge
