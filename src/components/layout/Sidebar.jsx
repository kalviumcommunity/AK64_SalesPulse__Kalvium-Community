import { NavLink } from 'react-router-dom'
import { X, Zap } from 'lucide-react'
import Button from '@/components/ui/Button'
import { sidebarActions, sidebarNavigation } from '@/constants/navigation'
import { cn } from '@/utils/cn'

function Sidebar({ isOpen, onClose }) {
  const linkClass = ({ isActive }) =>
    cn(
      'flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-semibold transition',
      isActive ? 'bg-blue-50 text-primary' : 'text-slate-600 hover:bg-slate-100 hover:text-secondary',
    )

  return (
    <>
      <div
        className={cn('fixed inset-0 z-40 bg-slate-950/40 lg:hidden', isOpen ? 'block' : 'hidden')}
        onClick={onClose}
      />
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-50 flex w-72 flex-col border-r border-border bg-white transition-transform lg:static lg:z-auto lg:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full',
        )}
      >
        <div className="flex h-16 items-center justify-between border-b border-border px-4">
          <NavLink to="/dashboard" className="flex items-center gap-3" onClick={onClose}>
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-white">
              <Zap className="h-5 w-5" />
            </div>
            <div>
              <p className="text-sm font-bold text-secondary">SalesPulse AI</p>
              <p className="text-xs text-slate-500">Behaviour Intelligence</p>
            </div>
          </NavLink>
          <Button variant="ghost" className="h-9 w-9 p-0 lg:hidden" onClick={onClose} aria-label="Close sidebar">
            <X className="h-5 w-5" />
          </Button>
        </div>
        <nav className="flex-1 space-y-1 px-3 py-4">
          {sidebarNavigation.map((item) => (
            <NavLink key={item.path} to={item.path} className={linkClass} onClick={onClose}>
              <item.icon className="h-5 w-5" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-border p-3">
          {sidebarActions.map((item) => (
            <NavLink key={item.label} to={item.path} className={linkClass} onClick={onClose}>
              <item.icon className="h-5 w-5" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </div>
      </aside>
    </>
  )
}

export default Sidebar
