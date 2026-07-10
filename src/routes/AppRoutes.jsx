import { Navigate, Route, Routes } from 'react-router-dom'
import AuthLayout from '@/layouts/AuthLayout'
import DashboardLayout from '@/layouts/DashboardLayout'
import MainLayout from '@/layouts/MainLayout'
import Activities from '@/pages/activities/Activities'
import Analytics from '@/pages/analytics/Analytics'
import Login from '@/pages/auth/Login'
import Register from '@/pages/auth/Register'
import Customers from '@/pages/customers/Customers'
import Dashboard from '@/pages/dashboard/Dashboard'
import Deals from '@/pages/deals/Deals'
import Home from '@/pages/Home'
import NotFound from '@/pages/NotFound'
import Recommendations from '@/pages/recommendations/Recommendations'
import Settings from '@/pages/settings/Settings'

function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Home />} />
      </Route>

      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Route>

      <Route element={<DashboardLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="/deals" element={<Deals />} />
        <Route path="/activities" element={<Activities />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/recommendations" element={<Recommendations />} />
        <Route path="/settings" element={<Settings />} />
      </Route>

      <Route path="/404" element={<NotFound />} />
      <Route path="*" element={<Navigate to="/404" replace />} />
    </Routes>
  )
}

export default AppRoutes
