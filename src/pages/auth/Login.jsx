import { Link } from 'react-router-dom'
import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'
import Input from '@/components/ui/Input'

function Login() {
  return (
    <Card className="w-full max-w-md">
      <h1 className="text-2xl font-bold text-secondary">Login</h1>
      <p className="mt-2 text-sm text-slate-500">Authentication UI placeholder for SalesPulse AI.</p>
      <div className="mt-6 space-y-4">
        <Input label="Email" type="email" placeholder="name@company.com" disabled />
        <Input label="Password" type="password" placeholder="Password" disabled />
        <Button className="w-full" disabled>Login Placeholder</Button>
      </div>
      <p className="mt-5 text-center text-sm text-slate-500">
        Need an account? <Link to="/register" className="font-semibold text-primary">Register</Link>
      </p>
    </Card>
  )
}

export default Login
