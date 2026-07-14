import { NavLink } from 'react-router-dom'
import { X, Zap } from 'lucide-react'
import Button from '@/components/ui/Button'
import { sidebarActions, sidebarNavigation } from '@/constants/navigation'
import { cn } from '@/utils/cn'
import { useAuth } from '@/contexts/AuthContext'

function Sidebar({ isOpen, onClose }) {
  const { logout, user } = useAuth()
  const role = user?.role?.toLowerCase()

  const visibleNav = sidebarNavigation.filter((item) => {
    if (item.path === '/team') {
      return role === 'manager' || role === 'admin'
    }
    return true
  })

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
          'fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-border bg-white transition-transform lg:static lg:z-auto lg:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full',
        )}
      >
        <div className="flex h-16 items-center justify-between border-b border-border px-4">
          <NavLink to="/performance" className="flex items-center gap-2.5" onClick={onClose}>
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-white">
              <Zap className="h-4 w-4" />
            </div>
            <div>
              <p className="text-sm font-bold text-secondary leading-tight">SalesPulse</p>
              <p className="text-xs text-slate-500 leading-tight">AI Platform</p>
            </div>
          </NavLink>
          <Button variant="ghost" className="h-8 w-8 p-0 lg:hidden" onClick={onClose} aria-label="Close sidebar">
            <X className="h-4 w-4" />
          </Button>
        </div>
        <nav className="flex-1 space-y-0.5 px-2 py-4">
          {visibleNav.map((item) => (
            <NavLink key={item.path} to={item.path} className={linkClass} onClick={onClose}>
              <item.icon className="h-4 w-4" />
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-border p-2">
          {sidebarActions.map((item) => {
            const isLogout = item.label === 'Logout'
            return (
              <NavLink
                key={item.label}
                to={item.path}
                className={linkClass}
                onClick={() => {
                  onClose()
                  if (isLogout) logout()
                }}
              >
                <item.icon className="h-4 w-4" />
                <span>{item.label}</span>
              </NavLink>
            )
          })}
        </div>
      </aside>
    </>
  )
}

export default Sidebar
