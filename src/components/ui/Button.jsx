import { cn } from '@/utils/cn'

const variants = {
  primary: 'bg-primary text-white hover:bg-accent focus-visible:outline-primary',
  secondary:
    'border border-border bg-white text-secondary hover:bg-slate-50 focus-visible:outline-primary',
  ghost: 'text-slate-600 hover:bg-slate-100 hover:text-secondary focus-visible:outline-primary',
}

function Button({
  as: Component = 'button',
  children,
  className,
  variant = 'primary',
  type = 'button',
  ...props
}) {
  const componentProps = Component === 'button' ? { type, ...props } : props

  return (
    <Component
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2',
        variants[variant],
        className,
      )}
      {...componentProps}
    >
      {children}
    </Component>
  )
}

export default Button
