export default function Notifications() {
  return (
    <main className="p-6">
      {/* Breadcrumb */}
      <nav className="mb-4 text-sm text-gray-500">
        <a href="/home" className="hover:text-gray-700">Home</a>
        <span className="mx-2">›</span>
        <span className="text-gray-700">Notifications</span>
      </nav>

      {/* Header */}
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
        <div className="hidden gap-2 sm:flex">
          <span className="rounded-full bg-gray-100 px-3 py-1 text-sm">All</span>
          <span className="rounded-full bg-blue-600 px-3 py-1 text-sm text-white">Unread</span>
          <span className="rounded-full bg-gray-100 px-3 py-1 text-sm">System</span>
        </div>
      </div>

      {/* List */}
      <section className="mx-auto max-w-3xl divide-y rounded-xl bg-white shadow">
        {/* Item (unread) */}
        <article className="flex items-start gap-4 p-4">
          <span className="mt-2 h-2 w-2 rounded-full bg-blue-600"></span>
          <div className="flex-1">
            <h3 className="font-medium text-gray-900">Forecast run completed</h3>
            <p className="text-sm text-gray-600">Scenario “Q2 Base” is ready. View the updated dashboard.</p>
          </div>
          <time className="text-xs text-gray-400">5m ago</time>
        </article>

        {/* Item */}
        <article className="flex items-start gap-4 p-4">
          <span className="mt-2 h-2 w-2 rounded-full bg-transparent"></span>
          <div className="flex-1">
            <h3 className="font-medium text-gray-900">Data upload successful</h3>
            <p className="text-sm text-gray-600">“sales_q1.csv” was processed with 2 warnings.</p>
          </div>
          <time className="text-xs text-gray-400">1h ago</time>
        </article>

        {/* Item */}
        <article className="flex items-start gap-4 p-4">
          <span className="mt-2 h-2 w-2 rounded-full bg-transparent"></span>
          <div className="flex-1">
            <h3 className="font-medium text-gray-900">Model retrained</h3>
            <p className="text-sm text-gray-600">New coefficients deployed for revenue forecaster.</p>
          </div>
          <time className="text-xs text-gray-400">Yesterday</time>
        </article>
      </section>

      {/* Footer actions */}
      <div className="mx-auto mt-4 max-w-3xl flex items-center justify-between">
        <button className="rounded border px-3 py-2 text-sm hover:bg-gray-50">Mark all as read</button>
        <a href="#" className="text-sm text-blue-600 hover:underline">View older</a>
      </div>
    </main>
  );
}
