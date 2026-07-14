import {
  Activity,
  Award,
  BrainCircuit,
  LayoutDashboard,
  LogOut,
  Settings,
  TrendingUp,
  Users,
} from 'lucide-react'

export const sidebarNavigation = [
  { label: 'Performance',      path: '/performance',      icon: LayoutDashboard },
  { label: 'Pipeline',         path: '/pipeline',         icon: TrendingUp },
  { label: 'Win/Loss',         path: '/win-loss',         icon: Award },
  { label: 'Behaviour',        path: '/behaviour',        icon: Activity },
  { label: 'Team',             path: '/team',             icon: Users },
  { label: 'Recommendations',  path: '/recommendations',  icon: BrainCircuit },
]

export const sidebarActions = [
  { label: 'Settings', path: '/settings', icon: Settings },
  { label: 'Logout',   path: '/login',    icon: LogOut },
]
