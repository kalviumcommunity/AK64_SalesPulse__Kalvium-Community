import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import AuthCard from '@/components/AuthCard'
import { cn } from '@/utils/cn'

function Signup() {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [role, setRole] = useState('Representative')
  const [errors, setErrors] = useState({})

  const handleSubmit = (e) => {
    e.preventDefault()

    const newErrors = {}
    if (!name.trim()) {
      newErrors.name = 'Name is required'
    }
    if (!email.trim()) {
      newErrors.email = 'Email is required'
    }
    if (!password) {
      newErrors.password = 'Password is required'
    }
    if (!confirmPassword) {
      newErrors.confirmPassword = 'Confirm Password is required'
    } else if (password && password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    setErrors(newErrors)

    if (Object.keys(newErrors).length > 0) {
      return
    }

    // Mock successful signup
    login(email, role, name)
    navigate('/performance')
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <AuthCard subtitle="Create your SalesPulse AI account">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1.5 text-xs font-semibold text-slate-700">
              Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="John Doe"
              className={cn(
                'w-full rounded-lg border bg-white px-3 py-2 text-sm text-text outline-none transition placeholder:text-slate-400 focus:border-primary focus:ring-4 focus:ring-blue-100',
                errors.name ? 'border-red-300 focus:border-red-500 focus:ring-red-100' : 'border-slate-200'
              )}
            />
            {errors.name && (
              <p className="mt-1 text-xs text-red-600 font-normal">
                {errors.name}
              </p>
            )}
          </div>

          <div>
            <label className="block mb-1.5 text-xs font-semibold text-slate-700">
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@company.com"
              className={cn(
                'w-full rounded-lg border bg-white px-3 py-2 text-sm text-text outline-none transition placeholder:text-slate-400 focus:border-primary focus:ring-4 focus:ring-blue-100',
                errors.email ? 'border-red-300 focus:border-red-500 focus:ring-red-100' : 'border-slate-200'
              )}
            />
            {errors.email && (
              <p className="mt-1 text-xs text-red-600 font-normal">
                {errors.email}
              </p>
            )}
          </div>

          <div>
            <label className="block mb-1.5 text-xs font-semibold text-slate-700">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className={cn(
                'w-full rounded-lg border bg-white px-3 py-2 text-sm text-text outline-none transition placeholder:text-slate-400 focus:border-primary focus:ring-4 focus:ring-blue-100',
                errors.password ? 'border-red-300 focus:border-red-500 focus:ring-red-100' : 'border-slate-200'
              )}
            />
            {errors.password && (
              <p className="mt-1 text-xs text-red-600 font-normal">
                {errors.password}
              </p>
            )}
          </div>

          <div>
            <label className="block mb-1.5 text-xs font-semibold text-slate-700">
              Confirm Password
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              className={cn(
                'w-full rounded-lg border bg-white px-3 py-2 text-sm text-text outline-none transition placeholder:text-slate-400 focus:border-primary focus:ring-4 focus:ring-blue-100',
                errors.confirmPassword ? 'border-red-300 focus:border-red-500 focus:ring-red-100' : 'border-slate-200'
              )}
            />
            {errors.confirmPassword && (
              <p className="mt-1 text-xs text-red-600 font-normal">
                {errors.confirmPassword}
              </p>
            )}
          </div>

          <div className="space-y-2 pt-1">
            <label className="block text-xs font-semibold text-slate-700 text-center">
              Role
            </label>
            <div className="flex justify-center gap-2">
              {['Representative', 'Manager', 'Admin'].map((r) => {
                const isSelected = role === r
                return (
                  <button
                    key={r}
                    type="button"
                    onClick={() => setRole(r)}
                    className={cn(
                      'rounded-full px-3 py-1 text-xs font-semibold ring-1 transition cursor-pointer',
                      isSelected
                        ? 'bg-blue-50 text-blue-600 ring-blue-200'
                        : 'bg-slate-50 text-slate-600 ring-slate-200 hover:bg-slate-100'
                    )}
                  >
                    {r}
                  </button>
                )
              })}
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 text-white rounded-lg py-2.5 text-sm font-semibold hover:bg-blue-700 transition cursor-pointer focus:outline-none focus:ring-4 focus:ring-blue-100 mt-4"
          >
            Create account
          </button>
        </form>

        <p className="mt-6 text-center text-xs text-slate-500">
          Already have an account?{' '}
          <Link to="/login" className="font-semibold text-blue-600 hover:underline">
            Log in
          </Link>
        </p>
      </AuthCard>
    </div>
  )
}

export default Signup
