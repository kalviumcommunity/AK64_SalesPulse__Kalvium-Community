import { cn } from '@/utils/cn'

function Card({ children, className }) {
  return (
    <section className={cn('rounded-xl border border-border bg-card p-5 shadow-sm', className)}>
      {children}
    </section>
  )
}

export default Card
