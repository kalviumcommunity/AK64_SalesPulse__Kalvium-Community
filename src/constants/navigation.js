import {
  Activity,
  BarChart3,
  BrainCircuit,
  Handshake,
  LayoutDashboard,
  LogOut,
  Settings,
  Users,
} from 'lucide-react'

export const sidebarNavigation = [
  { label: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { label: 'Customers', path: '/customers', icon: Users },
  { label: 'Deals', path: '/deals', icon: Handshake },
  { label: 'Activities', path: '/activities', icon: Activity },
  { label: 'Analytics', path: '/analytics', icon: BarChart3 },
  { label: 'AI Recommendations', path: '/recommendations', icon: BrainCircuit },
  { label: 'Settings', path: '/settings', icon: Settings },
]

export const sidebarActions = [
  { label: 'Logout', path: '/login', icon: LogOut },
]
