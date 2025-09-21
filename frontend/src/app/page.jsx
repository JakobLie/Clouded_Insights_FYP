export default function Landing() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-md p-8 space-y-6">
        {/* Header */}
        <header className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-gray-900">
            <span className="text-blue-600">TSH ERP APP</span>
          </h1>
        </header>

        {/* Links */}
        <div className="flex flex-col sm:flex-row sm:justify-center sm:gap-4 gap-3">
          <a
            href="/login"
            className="px-4 py-2 text-center bg-gray-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
          >
            Login
          </a>
          <a
            href="/setup"
            className="px-4 py-2 text-center bg-gray-600 text-white rounded-lg shadow hover:bg-green-700 transition"
          >
            Setup
          </a>
          <a
            href="/profit"
            className="px-4 py-2 text-center bg-gray-600 text-white rounded-lg shadow hover:bg-green-700 transition"
          >
            Home
          </a>
          <a
            href="/notifications"
            className="px-4 py-2 text-center bg-gray-600 text-white rounded-lg shadow hover:bg-purple-700 transition"
          >
            Notifications
          </a>
        </div>
      </div>
    </main>
  );
}
