import { Zap } from 'lucide-react'

function AuthCard({ children, subtitle }) {
  return (
    <div className="w-full max-w-sm bg-white rounded-xl shadow-sm p-8 border border-slate-100">
      <div className="flex flex-col items-center text-center mb-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary text-white mb-2">
          <Zap className="h-5 w-5" />
        </div>
        <div>
          <p className="text-sm font-bold text-secondary">SalesPulse AI</p>
          <p className="text-xs text-slate-500">Behaviour Intelligence</p>
        </div>
        
        {subtitle && (
          <p className="mt-5 text-sm text-slate-600 font-normal">{subtitle}</p>
        )}
      </div>
      {children}
    </div>
  )
}

export default AuthCard
