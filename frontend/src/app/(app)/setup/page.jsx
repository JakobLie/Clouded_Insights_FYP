"use client";
import { useSetup } from "../providers/SetupProvider";
import { useRouter } from "next/navigation";

export default function Setup() {

  const { setSalesTarget, setBudget } = useSetup();
  const router = useRouter();

  function handleSubmit(e) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const salesTarget = Number(form.get("salesTarget") || 0);
    const budget = Number(form.get("budget") || 0);
    setSalesTarget(salesTarget);
    setBudget(budget);
    router.push("/home");
  }

  return (
    <main className="p-6">
      {/* Breadcrumb + actions */}
      <div className="mb-6 flex items-center justify-between">
        <nav className="text-sm text-gray-500">
          <a href="/home" className="hover:text-gray-700">Home</a>
          <span className="mx-2">›</span>
          <span className="text-gray-700">Setup</span>
        </nav>
      </div>

      {/* Title */}
      <h1 className="mb-8 text-center text-2xl font-bold tracking-wide text-gray-800">
        SETUP
      </h1>

      {/* Form card */}
      <form onSubmit={handleSubmit} className="mx-auto max-w-4xl rounded-2xl bg-white p-8 shadow">
        <div className="grid gap-8 md:grid-cols-2">
          {/* Sales Target */}
          <div className="space-y-3">
            <h2 className="text-xl font-semibold text-gray-800">Sales Target</h2>
            <div className="rounded-xl border bg-gray-50 p-5">
              <label className="mb-2 block text-sm text-gray-600">Input Here (SGD)</label>
              <div className="relative">
                <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">$</span>
                <input
                  type="number" step="0.01" min="0.00"
                  placeholder="0.00"
                  name="salesTarget"
                  className="w-full rounded-lg border border-gray-300 bg-white py-2 pl-7 pr-3 outline-none focus:border-blue-500"
                />
              </div>
            </div>
          </div>

          {/* Cost Budget */}
          <div className="space-y-3">
            <h2 className="text-xl font-semibold text-gray-800">Cost Budget</h2>
            <div className="rounded-xl border bg-gray-50 p-5">
              <label className="mb-2 block text-sm text-gray-600">Input Here (SGD)</label>
              <div className="relative">
                <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">$</span>
                <input
                  type="number" step="0.01" min="0.00"
                  placeholder="0.00"
                  name="budget"
                  className="w-full rounded-lg border border-gray-300 bg-white py-2 pl-7 pr-3 outline-none focus:border-blue-500"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Run button */}
        <div className="mt-10 flex justify-center">
          <button
            type="submit"
            className="rounded-lg bg-green-600 px-6 py-3 font-medium text-white shadow hover:bg-green-700"
          >
            Run model
          </button>
        </div>
      </form>
    </main>
  );
}
