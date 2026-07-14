import { Navigate, Route, Routes } from 'react-router-dom'
import DashboardLayout from '@/layouts/DashboardLayout'
import MainLayout from '@/layouts/MainLayout'
import Home from '@/pages/Home'
import NotFound from '@/pages/NotFound'
import Login from '@/pages/Login'
import Signup from '@/pages/Signup'
import Performance from '@/pages/Performance'
import Pipeline from '@/pages/Pipeline'
import WinLoss from '@/pages/WinLoss'
import Behaviour from '@/pages/Behaviour'
import Team from '@/pages/Team'
import Recommendations from '@/pages/Recommendations'
import Settings from '@/pages/Settings'
import AuthGuard from '@/components/layout/AuthGuard'

function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Home />} />
      </Route>

      <Route path="/login"    element={<Login />} />
      <Route path="/signup"   element={<Signup />} />
      <Route path="/register" element={<Navigate to="/signup" replace />} />

      {/* Protected dashboard routes */}
      <Route element={<AuthGuard />}>
        <Route element={<DashboardLayout />}>
          <Route path="/performance"     element={<Performance />} />
          <Route path="/pipeline"        element={<Pipeline />} />
          <Route path="/win-loss"        element={<WinLoss />} />
          <Route path="/behaviour"       element={<Behaviour />} />
          <Route path="/team"            element={<Team />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/settings"        element={<Settings />} />
          {/* Legacy redirect */}
          <Route path="/dashboard"       element={<Navigate to="/performance" replace />} />
        </Route>
      </Route>

      <Route path="/404" element={<NotFound />} />
      <Route path="*"    element={<Navigate to="/404" replace />} />
    </Routes>
  )
}

export default AppRoutes
