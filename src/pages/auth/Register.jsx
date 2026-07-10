import { Link } from 'react-router-dom'
import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'
import Input from '@/components/ui/Input'

function Register() {
  return (
    <Card className="w-full max-w-md">
      <h1 className="text-2xl font-bold text-secondary">Register</h1>
      <p className="mt-2 text-sm text-slate-500">Account creation placeholder for future authentication.</p>
      <div className="mt-6 space-y-4">
        <Input label="Full name" placeholder="Sales Manager" disabled />
        <Input label="Work email" type="email" placeholder="name@company.com" disabled />
        <Input label="Password" type="password" placeholder="Password" disabled />
        <Button className="w-full" disabled>Register Placeholder</Button>
      </div>
      <p className="mt-5 text-center text-sm text-slate-500">
        Already registered? <Link to="/login" className="font-semibold text-primary">Login</Link>
      </p>
    </Card>
  )
}

export default Register
