import { Bell, Menu, Search } from 'lucide-react'
import Button from '@/components/ui/Button'

function Navbar({ onMenuClick }) {
  return (
    <header className="sticky top-0 z-30 border-b border-border bg-white">
      <div className="flex h-16 items-center justify-between gap-4 px-4 lg:px-6">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            className="h-10 w-10 p-0 lg:hidden"
            onClick={onMenuClick}
            aria-label="Open sidebar"
          >
            <Menu className="h-5 w-5" />
          </Button>
          <div className="hidden items-center gap-2 rounded-xl border border-border bg-slate-50 px-3 py-2 text-sm text-slate-500 md:flex md:w-80">
            <Search className="h-4 w-4" />
            <span>Search sales intelligence</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="ghost" className="h-10 w-10 p-0" aria-label="Notifications">
            <Bell className="h-5 w-5" />
          </Button>
          <div className="flex items-center gap-3">
            <div className="hidden text-right sm:block">
              <p className="text-sm font-semibold text-secondary">Sales Team</p>
              <p className="text-xs text-slate-500">Workspace</p>
            </div>
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-sm font-bold text-white">
              SP
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Navbar
