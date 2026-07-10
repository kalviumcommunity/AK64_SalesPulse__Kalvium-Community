import { Link } from 'react-router-dom'
import Button from '@/components/ui/Button'

function NotFound() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-background px-4 text-center">
      <div>
        <p className="text-sm font-semibold uppercase text-primary">404</p>
        <h1 className="mt-3 text-3xl font-bold text-secondary">Page not found</h1>
        <p className="mt-3 text-sm text-slate-500">The requested SalesPulse AI page does not exist.</p>
        <Button as={Link} to="/dashboard" className="mt-6">
          Return to Dashboard
        </Button>
      </div>
    </main>
  )
}

export default NotFound
