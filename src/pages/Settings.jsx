import { useState } from 'react'
import { User, Bell, Shield, Palette, Save } from 'lucide-react'
import Card from '@/components/ui/Card'
import { useAuth } from '@/contexts/AuthContext'
import { cn } from '@/utils/cn'

const TABS = [
  { id: 'profile',        label: 'Profile',        icon: User },
  { id: 'notifications',  label: 'Notifications',  icon: Bell },
  { id: 'security',       label: 'Security',       icon: Shield },
  { id: 'appearance',     label: 'Appearance',     icon: Palette },
]

function InputRow({ label, description, children }) {
  return (
    <div className="flex items-start justify-between gap-6 py-4 border-b border-border last:border-0">
      <div className="min-w-0 flex-1">
        <p className="text-sm font-semibold text-secondary">{label}</p>
        {description && <p className="text-xs text-slate-500 mt-0.5">{description}</p>}
      </div>
      <div className="w-64 shrink-0">{children}</div>
    </div>
  )
}

function Toggle({ checked, onChange }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={cn(
        'relative inline-flex h-5 w-9 cursor-pointer rounded-full transition-colors focus:outline-none focus:ring-4 focus:ring-blue-100',
        checked ? 'bg-primary' : 'bg-slate-200'
      )}
    >
      <span className={cn(
        'inline-block h-4 w-4 translate-y-0.5 rounded-full bg-white shadow transition-transform',
        checked ? 'translate-x-4' : 'translate-x-0.5'
      )} />
    </button>
  )
}

export default function Settings() {
  const { user } = useAuth()
  const [tab, setTab] = useState('profile')
  const [saved, setSaved] = useState(false)

  // Profile state
  const [name,     setName]     = useState(user?.name  || '')
  const [email,    setEmail]    = useState(user?.email || '')

  // Notification state
  const [emailAlerts,   setEmailAlerts]   = useState(true)
  const [dealAlerts,    setDealAlerts]    = useState(true)
  const [coachingAlerts, setCoachingAlerts] = useState(true)
  const [weeklyDigest,  setWeeklyDigest]  = useState(false)

  // Security state
  const [currentPw, setCurrentPw] = useState('')
  const [newPw,     setNewPw]     = useState('')
  const [confirmPw, setConfirmPw] = useState('')

  // Appearance
  const [theme,    setTheme]    = useState('light')
  const [density,  setDensity]  = useState('comfortable')

  const handleSave = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 2500)
  }

  const inputCls = 'w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-text outline-none transition focus:border-primary focus:ring-4 focus:ring-blue-100'

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold text-secondary">Settings</h1>
        <p className="mt-1 text-sm text-slate-500">Manage your account preferences and workspace configuration.</p>
      </div>

      {/* Tab nav */}
      <div className="flex gap-1 border-b border-border">
        {TABS.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            className={cn(
              'flex items-center gap-2 px-4 py-2.5 text-sm font-semibold transition border-b-2 cursor-pointer -mb-px',
              tab === t.id
                ? 'border-primary text-primary'
                : 'border-transparent text-slate-500 hover:text-secondary'
            )}
          >
            <t.icon className="h-4 w-4" />
            {t.label}
          </button>
        ))}
      </div>

      {/* Profile */}
      {tab === 'profile' && (
        <Card>
          <div className="flex items-center gap-4 pb-4 border-b border-border mb-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary text-lg font-bold text-white">
              {(name || 'SP').split(' ').map((n) => n[0]).join('').slice(0, 2).toUpperCase()}
            </div>
            <div>
              <p className="text-sm font-semibold text-secondary">{name || 'Your Name'}</p>
              <span className="mt-0.5 inline-block rounded-full bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-600 capitalize">
                {user?.role || 'Representative'}
              </span>
            </div>
          </div>
          <InputRow label="Full Name" description="Your display name across the platform.">
            <input value={name} onChange={(e) => setName(e.target.value)} className={inputCls} placeholder="Jane Smith" />
          </InputRow>
          <InputRow label="Email Address" description="Used for login and notifications.">
            <input value={email} onChange={(e) => setEmail(e.target.value)} className={inputCls} placeholder="jane@company.com" type="email" />
          </InputRow>
          <InputRow label="Role" description="Your role is set by your admin and cannot be changed here.">
            <div className={cn(inputCls, 'bg-slate-50 text-slate-500 cursor-not-allowed capitalize')}>
              {user?.role || 'Representative'}
            </div>
          </InputRow>
        </Card>
      )}

      {/* Notifications */}
      {tab === 'notifications' && (
        <Card>
          <InputRow label="Email Alerts" description="Receive emails for urgent deal and behaviour flags.">
            <Toggle checked={emailAlerts} onChange={setEmailAlerts} />
          </InputRow>
          <InputRow label="Deal Alerts" description="Notify me when a deal is flagged as stalled or at risk.">
            <Toggle checked={dealAlerts} onChange={setDealAlerts} />
          </InputRow>
          <InputRow label="Coaching Recommendations" description="Notify me when new AI coaching tips are generated.">
            <Toggle checked={coachingAlerts} onChange={setCoachingAlerts} />
          </InputRow>
          <InputRow label="Weekly Digest" description="A summary email of your performance every Monday.">
            <Toggle checked={weeklyDigest} onChange={setWeeklyDigest} />
          </InputRow>
        </Card>
      )}

      {/* Security */}
      {tab === 'security' && (
        <Card>
          <InputRow label="Current Password" description="">
            <input type="password" value={currentPw} onChange={(e) => setCurrentPw(e.target.value)} className={inputCls} placeholder="••••••••" />
          </InputRow>
          <InputRow label="New Password" description="At least 8 characters.">
            <input type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} className={inputCls} placeholder="••••••••" />
          </InputRow>
          <InputRow label="Confirm New Password" description="">
            <input type="password" value={confirmPw} onChange={(e) => setConfirmPw(e.target.value)} className={inputCls} placeholder="••••••••" />
          </InputRow>
        </Card>
      )}

      {/* Appearance */}
      {tab === 'appearance' && (
        <Card>
          <InputRow label="Theme" description="Choose your interface colour scheme.">
            <select value={theme} onChange={(e) => setTheme(e.target.value)} className={inputCls}>
              <option value="light">Light</option>
              <option value="dark">Dark (coming soon)</option>
              <option value="system">System Default</option>
            </select>
          </InputRow>
          <InputRow label="Display Density" description="Control how compact the UI feels.">
            <select value={density} onChange={(e) => setDensity(e.target.value)} className={inputCls}>
              <option value="comfortable">Comfortable</option>
              <option value="compact">Compact</option>
            </select>
          </InputRow>
        </Card>
      )}

      {/* Save button */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={handleSave}
          className="flex items-center gap-2 rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 transition cursor-pointer focus:outline-none focus:ring-4 focus:ring-blue-100"
        >
          <Save className="h-4 w-4" />
          Save Changes
        </button>
        {saved && (
          <span className="text-sm text-emerald-600 font-semibold animate-fade-in">
            ✓ Changes saved
          </span>
        )}
      </div>
    </div>
  )
}
