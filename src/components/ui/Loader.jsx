function Loader({ label = 'Loading' }) {
  return (
    <div className="flex items-center gap-3 text-sm font-medium text-slate-600">
      <span className="h-5 w-5 animate-spin rounded-full border-2 border-border border-t-primary" />
      <span>{label}</span>
    </div>
  )
}

export default Loader
