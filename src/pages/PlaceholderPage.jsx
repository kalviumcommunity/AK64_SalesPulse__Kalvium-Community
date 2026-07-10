import EmptyState from '@/components/common/EmptyState'
import PageHeader from '@/components/layout/PageHeader'

function PlaceholderPage({ title, description }) {
  return (
    <div className="space-y-6">
      <PageHeader title={title} description={description} />
      <EmptyState
        title={`${title} workspace is ready`}
        description="Business logic and backend-powered data will be connected in the next project phase."
      />
    </div>
  )
}

export default PlaceholderPage
