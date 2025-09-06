export default function Upload() {
  return (
    <main className="p-6">
      {/* Breadcrumb */}
      <nav className="mb-4 text-sm text-gray-500">
        <a href="/home" className="hover:text-gray-700">Home</a>
        <span className="mx-2">›</span>
        <span className="text-gray-700">Upload</span>
      </nav>

      {/* Title */}
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Upload CSV</h1>

      {/* Card */}
      <section className="mx-auto max-w-2xl rounded-xl bg-white p-8 shadow">
        <form className="space-y-6" action="/api/upload" method="post">
          {/* Dropzone look (static) */}
          <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 p-10 text-center">
            <svg className="mb-3 h-10 w-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6h.6a4.5 4.5 0 010 9H7z" />
            </svg>
            <p className="text-sm text-gray-600">
              Drag & drop your file here, or{" "}
              <label className="cursor-pointer text-blue-600 underline">
                browse
                <input type="file" name="file" accept=".csv" className="hidden" />
              </label>
            </p>
            <p className="mt-1 text-xs text-gray-400">Accepted: .csv • Max 10MB</p>
          </div>

          {/* Options */}
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Dataset name</label>
              <input type="text" name="dataset" placeholder="e.g. Q2 Sales"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label className="mb-1 block text-sm font-medium text-gray-700">Delimiter</label>
              <select name="delimiter"
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
                <option value=",">Comma (,)</option>
                <option value=";">Semicolon (;)</option>
                <option value="\t">Tab</option>
              </select>
            </div>
          </div>

          {/* Submit */}
          <div className="flex items-center justify-between">
            <p className="text-xs text-gray-500">We’ll validate column headers after upload.</p>
            <button type="submit" className="rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-700">
              Upload
            </button>
          </div>
        </form>
      </section>
    </main>
  );
}
