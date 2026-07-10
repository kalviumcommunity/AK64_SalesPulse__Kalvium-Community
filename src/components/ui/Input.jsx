import { cn } from '@/utils/cn'

function Input({ className, label, id, error, ...props }) {
  const inputId = id || props.name

  return (
    <label className="block">
      {label && (
        <span className="mb-2 block text-sm font-medium text-slate-700">
          {label}
        </span>
      )}
      <input
        id={inputId}
        className={cn(
          'w-full rounded-xl border border-border bg-white px-3.5 py-2.5 text-sm text-text outline-none transition placeholder:text-slate-400 focus:border-primary focus:ring-4 focus:ring-blue-100',
          error && 'border-red-300 focus:border-red-500 focus:ring-red-100',
          className,
        )}
        {...props}
      />
      {error && <span className="mt-1.5 block text-xs text-red-600">{error}</span>}
    </label>
  )
}

export default Input
