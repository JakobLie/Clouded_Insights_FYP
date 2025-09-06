export default function Landing() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="max-w-2xl w-full bg-white rounded-2xl shadow-md p-8 space-y-6">
        {/* Header */}
        <header className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome to <span className="text-blue-600">TSH ERP App</span>
          </h1>
          <h2 className="text-lg text-gray-600">
            This will be the landing page
          </h2>
        </header>

        {/* Details Section */}
        <section>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">
            Landing Page Details:
          </h3>
          <ul className="list-disc list-inside text-gray-600 space-y-1">
            <li>Direct to Login Page</li>
            <li>Direct to Signup Page</li>
            <li>Direct to Dashboard Home Page</li>
            <li>Direct to Notifications Page</li>
            <li>Brief intro to App</li>
          </ul>
        </section>

        {/* Links */}
        <div className="flex flex-col sm:flex-row sm:justify-center sm:gap-4 gap-3">
          <a
            href="/login"
            className="px-4 py-2 text-center bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
          >
            Go to Login
          </a>
          <a
            href="/login"
            className="px-4 py-2 text-center bg-orange-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
          >
            Go to Signup
          </a>
          <a
            href="/setup"
            className="px-4 py-2 text-center bg-pink-600 text-white rounded-lg shadow hover:bg-green-700 transition"
          >
            Go to Dashboard Setup page
          </a>
          <a
            href="/home"
            className="px-4 py-2 text-center bg-green-600 text-white rounded-lg shadow hover:bg-green-700 transition"
          >
            Go to Dashboard Home page
          </a>
          <a
            href="/notifications"
            className="px-4 py-2 text-center bg-purple-600 text-white rounded-lg shadow hover:bg-purple-700 transition"
          >
            Go to Notifications
          </a>
        </div>
      </div>
    </main>
  );
}
