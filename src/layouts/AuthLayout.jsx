import { Outlet } from 'react-router-dom'

function AuthLayout() {
  return (
    <main className="grid min-h-screen bg-background px-4 py-10 sm:px-6 lg:grid-cols-[1fr_1.1fr] lg:px-0 lg:py-0">
      <section className="hidden bg-secondary p-10 text-white lg:flex lg:flex-col lg:justify-between">
        <div className="text-xl font-bold">SalesPulse AI</div>
        <div>
          <h1 className="max-w-xl text-4xl font-bold leading-tight">
            AI-powered sales behaviour intelligence for modern revenue teams.
          </h1>
          <p className="mt-4 max-w-lg text-sm leading-6 text-slate-300">
            Frontend foundation prepared for secure auth, customer intelligence,
            deal activity, analytics, and recommendations.
          </p>
        </div>
        <p className="text-xs text-slate-400">Day 2 frontend foundation</p>
      </section>
      <section className="flex items-center justify-center">
        <Outlet />
      </section>
    </main>
  )
}

export default AuthLayout
