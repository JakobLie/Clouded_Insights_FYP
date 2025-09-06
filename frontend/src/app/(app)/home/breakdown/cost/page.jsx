export default function cost() {
    //return <h1>COST PAGE</h1>;
    return (
    <main className="p-4 md:p-6">
      {/* Breadcrumb */}
      <nav className="mb-4 text-sm text-gray-500">
        <a href="/home" className="hover:text-gray-700">Home</a>
        <span className="mx-2">›</span>
        <a href="/breakdown" className="hover:text-gray-700">Breakdown</a>
        <span className="mx-2">›</span>
        <span className="text-gray-700">Cost Dashboard</span>
      </nav>

      {/* Layout: left list + right chart panel */}
      <section className="grid grid-cols-1 md:grid-cols-[300px,1fr] gap-4 md:gap-6">
        {/* Left: categories (scrollable) */}
        <aside className="md:h-[70vh] overflow-y-auto pr-1">
          {/* Active card */}
          <a
            href="#"
            className="block rounded-xl border-2 border-black bg-orange-200 px-4 py-5 shadow mb-4"
          >
            <div className="text-center font-semibold leading-6">
              <div>Cost CAT 1</div>
              <div>FORECASTED VALUE</div>
              <div>(XX %)</div>
            </div>
          </a>

          {/* Inactive cards */}
          <a href="#" className="block rounded-xl bg-green-200 px-4 py-5 shadow mb-4">
            <div className="text-center font-semibold leading-6">
              <div>Cost CAT 2</div>
              <div>FORECASTED VALUE</div>
              <div>(XX %)</div>
            </div>
          </a>

          <a href="#" className="block rounded-xl bg-green-200 px-4 py-5 shadow mb-4">
            <div className="text-center font-semibold leading-6">
              <div>Cost CAT 3</div>
              <div>FORECASTED VALUE</div>
              <div>(XX %)</div>
            </div>
          </a>

          <a href="#" className="block rounded-xl bg-green-200 px-4 py-5 shadow">
            <div className="text-center font-semibold leading-6">
              <div>Cost CAT 4</div>
              <div>FORECASTED VALUE</div>
              <div>(XX %)</div>
            </div>
          </a>
        </aside>

        {/* Right: chart panel */}
        <section className="flex flex-col">
          {/* Chart area with range toggle */}
          <div className="relative rounded-lg bg-orange-200 p-4 md:p-6 flex-1 min-h-[320px]">
            {/* Range toggle (top-right) */}
            <div className="absolute right-3 top-3 inline-flex rounded border border-gray-400 overflow-hidden">
              <a href="#" className="px-3 py-1 text-sm bg-white hover:bg-gray-100">3M</a>
              <a href="#" className="px-3 py-1 text-sm bg-gray-900 text-white">6M</a>
              <a href="#" className="px-3 py-1 text-sm bg-white hover:bg-gray-100">12M</a>
            </div>

            {/* Placeholder text */}
            <div className="h-full w-full flex items-center justify-center text-center text-gray-800 font-semibold">
              GRAPH OF Cost CAT 1 FORECASTED + HISTORICAL VALUES
            </div>
          </div>

          {/* Simulate button */}
          <div className="mt-3">
            <button className="rounded border px-4 py-2 bg-white hover:bg-gray-50">
              SIMULATE
            </button>
          </div>
        </section>
      </section>
    </main>
  );
}