import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Bell, Menu, Search, X, LogOut, ChevronDown } from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'

const SEARCH_INDEX = [
  // Pages
  { type: 'Page',   label: 'Performance Dashboard', path: '/performance',  desc: 'Sales KPIs and rep performance' },
  { type: 'Page',   label: 'Pipeline Analytics',     path: '/pipeline',     desc: 'Open deals and stage breakdown' },
  { type: 'Page',   label: 'Win/Loss Analysis',      path: '/win-loss',     desc: 'Historical deal outcomes' },
  { type: 'Page',   label: 'Behaviour Analytics',    path: '/behaviour',    desc: 'Response time and tone metrics' },
  { type: 'Page',   label: 'Team Performance',       path: '/team',         desc: 'Manager quota rollup' },
  // Deals
  { type: 'Deal',   label: 'Cloud Suite License',    path: '/pipeline',     desc: 'Stark Industries — Proposal' },
  { type: 'Deal',   label: 'Hardware Fleet Renewal', path: '/pipeline',     desc: 'Wayne Enterprises — Negotiation' },
  { type: 'Deal',   label: 'API Support SLA',        path: '/pipeline',     desc: 'GlobalTech Ltd — Discovery' },
  { type: 'Deal',   label: 'SaaS Analytics Package', path: '/pipeline',     desc: 'Acme Corp — Closing' },
  // Customers
  { type: 'Customer', label: 'Stark Industries',     path: '/pipeline',     desc: 'Enterprise · robert@stark.com' },
  { type: 'Customer', label: 'Wayne Enterprises',    path: '/pipeline',     desc: 'Enterprise · bruce@wayne.com' },
  { type: 'Customer', label: 'Acme Corp',            path: '/pipeline',     desc: 'Mid-Market · Positive sentiment' },
  { type: 'Customer', label: 'GlobalTech Ltd',       path: '/pipeline',     desc: 'Mid-Market · Neutral sentiment' },
  // Reps
  { type: 'Rep',    label: 'Sarah Jenkins',          path: '/performance',  desc: 'Rep · Quota 124% · Excellent' },
  { type: 'Rep',    label: 'Michael Chen',           path: '/performance',  desc: 'Rep · Quota 103% · On Track' },
  { type: 'Rep',    label: 'David Miller',           path: '/behaviour',    desc: 'Rep · Response time flagged' },
  { type: 'Rep',    label: 'Emma Watson',            path: '/behaviour',    desc: 'Rep · Follow-up rate low' },
]

const TYPE_COLORS = {
  Page:     'bg-blue-50 text-blue-600',
  Deal:     'bg-emerald-50 text-emerald-700',
  Customer: 'bg-purple-50 text-purple-700',
  Rep:      'bg-amber-50 text-amber-700',
}

export default function Navbar({ onMenuClick }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const inputRef = useRef(null)
  const containerRef = useRef(null)
  const userMenuRef = useRef(null)

  const initials = user?.name
    ? user.name.split(' ').map((n) => n[0]).join('').slice(0, 2).toUpperCase()
    : 'SP'

  const results = query.trim().length >= 1
    ? SEARCH_INDEX.filter(
        (item) =>
          item.label.toLowerCase().includes(query.toLowerCase()) ||
          item.desc.toLowerCase().includes(query.toLowerCase())
      ).slice(0, 7)
    : []

  const handleSelect = (item) => {
    navigate(item.path)
    setQuery('')
    setOpen(false)
  }

  // Close search dropdown on outside click
  useEffect(() => {
    function handler(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  // Close user menu on outside click
  useEffect(() => {
    function handler(e) {
      if (userMenuRef.current && !userMenuRef.current.contains(e.target)) {
        setUserMenuOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const handleLogout = () => {
    setUserMenuOpen(false)
    logout()
    navigate('/login')
  }

  // Keyboard shortcut Ctrl+K / Cmd+K
  useEffect(() => {
    function handler(e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault()
        inputRef.current?.focus()
        setOpen(true)
      }
      if (e.key === 'Escape') {
        setOpen(false)
        setQuery('')
      }
    }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [])

  return (
    <header className="sticky top-0 z-30 border-b border-border bg-white">
      <div className="flex h-16 items-center justify-between gap-4 px-4 lg:px-6">
        <div className="flex items-center gap-3">
          <button
            type="button"
            className="flex h-10 w-10 items-center justify-center rounded-xl text-slate-600 hover:bg-slate-100 transition cursor-pointer lg:hidden"
            onClick={onMenuClick}
            aria-label="Open sidebar"
          >
            <Menu className="h-5 w-5" />
          </button>

          {/* Search */}
          <div ref={containerRef} className="relative hidden md:block">
            <div className="flex items-center gap-2 rounded-xl border border-border bg-slate-50 px-3 py-2 w-80 focus-within:border-primary focus-within:ring-4 focus-within:ring-blue-100 transition">
              <Search className="h-4 w-4 text-slate-400 shrink-0" />
              <input
                ref={inputRef}
                type="text"
                value={query}
                onChange={(e) => { setQuery(e.target.value); setOpen(true) }}
                onFocus={() => setOpen(true)}
                placeholder="Search sales intelligence…"
                className="flex-1 bg-transparent text-sm text-text outline-none placeholder:text-slate-400"
              />
              {query && (
                <button type="button" onClick={() => { setQuery(''); setOpen(false) }} className="text-slate-400 hover:text-slate-600 transition cursor-pointer">
                  <X className="h-3.5 w-3.5" />
                </button>
              )}
              {!query && (
                <span className="text-xs text-slate-400 shrink-0 border border-slate-200 rounded px-1.5 py-0.5 font-mono">⌘K</span>
              )}
            </div>

            {/* Dropdown */}
            {open && results.length > 0 && (
              <div className="absolute top-full left-0 mt-2 w-full bg-white rounded-xl border border-border shadow-lg overflow-hidden z-50">
                {results.map((item, i) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => handleSelect(item)}
                    className="w-full flex items-start gap-3 px-4 py-2.5 hover:bg-slate-50 transition text-left cursor-pointer"
                  >
                    <span className={`mt-0.5 shrink-0 rounded-full px-2 py-0.5 text-xs font-semibold ${TYPE_COLORS[item.type]}`}>
                      {item.type}
                    </span>
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-secondary truncate">{item.label}</p>
                      <p className="text-xs text-slate-500 truncate">{item.desc}</p>
                    </div>
                  </button>
                ))}
              </div>
            )}

            {open && query.trim().length >= 1 && results.length === 0 && (
              <div className="absolute top-full left-0 mt-2 w-full bg-white rounded-xl border border-border shadow-lg px-4 py-4 text-sm text-slate-400 z-50">
                No results for "<span className="text-slate-600 font-medium">{query}</span>"
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            className="flex h-10 w-10 items-center justify-center rounded-xl text-slate-600 hover:bg-slate-100 transition cursor-pointer"
            aria-label="Notifications"
          >
            <Bell className="h-6 w-6" />
          </button>

          {/* User avatar + dropdown */}
          <div ref={userMenuRef} className="relative">
            <button
              type="button"
              onClick={() => setUserMenuOpen((v) => !v)}
              className="flex items-center gap-2.5 rounded-xl px-2 py-1.5 hover:bg-slate-100 transition cursor-pointer"
              aria-label="User menu"
            >
              <div className="hidden text-right sm:block">
                <p className="text-sm font-semibold text-secondary leading-tight">{user?.name || 'Sales Team'}</p>
                <p className="text-xs text-slate-500 capitalize leading-tight">{user?.role || 'Workspace'}</p>
              </div>
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-sm font-bold text-white shrink-0">
                {initials}
              </div>
              <ChevronDown className={`h-3.5 w-3.5 text-slate-400 transition-transform ${userMenuOpen ? 'rotate-180' : ''}`} />
            </button>

            {/* Dropdown menu */}
            {userMenuOpen && (
              <div className="absolute right-0 top-full mt-2 w-56 bg-white rounded-xl border border-border shadow-lg overflow-hidden z-50">
                <div className="px-4 py-3 border-b border-border">
                  <p className="text-sm font-semibold text-secondary truncate">{user?.name || 'Sales Team'}</p>
                  <p className="text-xs text-slate-500 truncate">{user?.email || ''}</p>
                  <span className="mt-1 inline-block rounded-full bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-600 capitalize">
                    {user?.role || 'Representative'}
                  </span>
                </div>
                <div className="p-1.5">
                  <button
                    type="button"
                    onClick={handleLogout}
                    className="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-sm font-semibold text-red-600 hover:bg-red-50 transition cursor-pointer"
                  >
                    <LogOut className="h-4 w-4" />
                    Sign out
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
