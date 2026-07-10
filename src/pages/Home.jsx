import { Link } from 'react-router-dom'
import { ArrowRight, BarChart3, BrainCircuit, Users } from 'lucide-react'
import Button from '@/components/ui/Button'
import Card from '@/components/ui/Card'

function Home() {
  return (
    <section className="mx-auto flex min-h-screen w-full max-w-6xl flex-col justify-center px-4 py-10 sm:px-6">
      <div className="max-w-3xl">
        <p className="text-sm font-semibold uppercase text-primary">SalesPulse AI</p>
        <h1 className="mt-4 text-4xl font-bold text-secondary sm:text-5xl">
          Sales Behaviour Intelligence Platform
        </h1>
        <p className="mt-5 text-base leading-7 text-slate-600">
          A production-ready React foundation for sales dashboards, customer
          insights, deal monitoring, activity tracking, analytics, and AI recommendations.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Button as={Link} to="/dashboard">
            Open Dashboard <ArrowRight className="h-4 w-4" />
          </Button>
          <Button as={Link} to="/login" variant="secondary">
            Login Placeholder
          </Button>
        </div>
      </div>
      <div className="mt-10 grid gap-4 md:grid-cols-3">
        {[
          { title: 'Customer Intelligence', icon: Users },
          { title: 'Sales Analytics', icon: BarChart3 },
          { title: 'AI Recommendations', icon: BrainCircuit },
        ].map((item) => (
          <Card key={item.title}>
            <item.icon className="h-6 w-6 text-primary" />
            <h2 className="mt-4 text-base font-semibold text-secondary">{item.title}</h2>
            <p className="mt-2 text-sm text-slate-500">Frontend placeholder module ready for Day 3 integration.</p>
          </Card>
        ))}
      </div>
    </section>
  )
}

export default Home
