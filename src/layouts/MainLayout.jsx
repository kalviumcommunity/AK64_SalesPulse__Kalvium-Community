import { Outlet } from 'react-router-dom'

function MainLayout() {
  return (
    <main className="min-h-screen bg-background text-text">
      <Outlet />
    </main>
  )
}

export default MainLayout
