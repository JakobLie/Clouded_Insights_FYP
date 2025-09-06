"use client";
import Link from "next/link"
import { useSetup } from "../providers/SetupProvider";
import { formatCurrency } from "../../../../utils/currency-utils"

export default function Home() {
  const { salesTarget, budget } = useSetup();
  const profitTarget = salesTarget - budget;
  const predProfit = 15150000;

  const quantitativeGrowth = predProfit - profitTarget;
  const percentageGrowth = (quantitativeGrowth/profitTarget)*100;

  // Decide box colours
  let predTitleClass = "text-center text-xl font-semibold ";
  let predTextClass = "flex items-start gap-3 ";
  let predBoxClass = "rounded-xl p-6 shadow-sm border ";
  if (percentageGrowth <= -5) {
    // Red = bad
    predTitleClass += "text-red-700"
    predTextClass += "text-red-900"
    predBoxClass += "border-red-200 bg-red-50 text-red-900";
  } else if (percentageGrowth > 0) {
    // Green = good
    predTitleClass += "text-green-700"
    predTextClass += "text-green-900"
    predBoxClass += "border-green-200 bg-green-50 text-green-900";
  } else {
    // Orange = warning
    predTitleClass += "text-orange-700"
    predTextClass += "text-orange-900"
    predBoxClass += "border-orange-200 bg-orange-50 text-orange-900";
  }

  return (
    <main className="p-6">
      {/* Breadcrumb */}
      <nav className="mb-4 text-sm text-gray-500">
        <a href="/home" className="hover:text-gray-700">Home</a>
      </nav>

      {/* Title */}
      <h1 className="mb-10 text-center text-2xl font-bold tracking-wide text-gray-800">
        PROFIT
      </h1>

      {/* Two-column summary */}
      <section className="mx-auto max-w-5xl grid gap-8 md:grid-cols-2">
        {/* profitTarget */}
        <div className="space-y-3">
          <h2 className="text-center text-xl font-semibold text-balck-700">Target</h2>

          <div className="rounded-xl border border-gray-200 bg-gray-50 p-6 shadow-sm">
            <div className="flex items-center gap-3 text-gray-700">
              <span className="text-lg">+</span>
              <span className="text-2xl font-semibold">${formatCurrency(profitTarget)}</span>
            </div>
          </div>
        </div>

        {/* predProfit */}
        <div className="space-y-3">
          <h2 className={predTitleClass}>Predicted</h2>

          <Link href="/home/breakdown">
            <div className={predBoxClass}>
              <div className={predTextClass}>
                <span className="text-lg">{predProfit >= 0 ? "+" : "-"}</span>
                <div className="leading-6">
                  <div className="text-2xl font-semibold">${formatCurrency(predProfit)}</div>
                  <div className="text-sm">{percentageGrowth.toFixed(1)}% growth</div>
                  <div className="text-sm">{quantitativeGrowth >= 0 ? "+" : "-"} ${formatCurrency(quantitativeGrowth)}</div>
                </div>
              </div>
            </div>
          </Link>
        </div>
      </section>
    </main>
  );
}
