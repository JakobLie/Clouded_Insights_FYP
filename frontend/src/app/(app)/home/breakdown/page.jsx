"use client";
import { useSetup } from "../../providers/SetupProvider";

import { formatCurrency } from "../../../../../utils/currency-utils";

import Link from "next/link";

export default function Breakdown() {
  const {salesTarget, budget } = useSetup();
  const predSales = 24830000;
  const predCost = 10655000;

  const amountBeyondSalesTarget = predSales - salesTarget;
  const percentageBeyondSalesTarget = (amountBeyondSalesTarget/predSales)*100;

  const costBeyondBudget = predCost - budget;
  const percentageCostBeyondBudget = (costBeyondBudget/predCost)*100;

  return (
    <main className="p-6">
      {/* Breadcrumb */}
      <nav className="mb-4 text-sm text-gray-500">
        <a href="/home" className="hover:text-gray-700">Home</a>
        <span className="mx-2">›</span>
        <span className="text-gray-700">Breakdown</span>
      </nav>

      {/* Title */}
      <h1 className="mb-10 text-center text-2xl font-bold tracking-wide text-gray-800">
        BREAKDOWN
      </h1>

      {/* Two panels with a vertical divider */}
      <section className="mx-auto max-w-6xl grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12">
        {/* Sales */}
        <div className="pr-0 md:pr-8 md:border-r md:border-gray-200">
          <h2 className="mb-8 text-center text-3xl font-semibold text-gray-900">Sales</h2>

          {/* Target card */}
          <div className="mb-10">
            <h3 className="mb-3 text-center text-lg font-medium text-gray-700">Target</h3>
            <div className="rounded-xl border border-gray-200 bg-gray-100 p-6 shadow-sm">
              <div className="flex items-center gap-3 text-gray-700">
                <span className="text-lg">+</span>
                <span className="text-xl font-semibold">${formatCurrency(salesTarget)}</span>
              </div>
            </div>
          </div>

          {/* Predicted card (orange) */}
          <Link href="/home/breakdown/sales">
            <div>
              <h3 className="mb-3 text-center text-lg font-medium text-orange-600">Predicted</h3>
              <div className="rounded-xl border border-orange-200 bg-orange-200/70 p-6 shadow-sm">
                <div className="flex items-start gap-3 text-orange-900">
                  <span className="text-lg">+</span>
                  <div className="leading-6">
                    <div className="text-xl font-semibold">${formatCurrency(predSales)}</div>
                    <div className="text-sm">{percentageBeyondSalesTarget.toFixed(1)}% beyond target</div>
                    <div className="text-sm">{amountBeyondSalesTarget > 0 ? "+" : "-"} ${formatCurrency(amountBeyondSalesTarget)}</div>
                  </div>
                </div>
              </div>
            </div>
          </Link>
        </div>

        {/* Cost */}
        <div className="pl-0 md:pl-8">
          <h2 className="mb-8 text-center text-3xl font-semibold text-gray-900">Cost</h2>

          {/* Budget card */}
          <div className="mb-10">
            <h3 className="mb-3 text-center text-lg font-medium text-gray-700">Budget</h3>
            <div className="rounded-xl border border-gray-200 bg-gray-100 p-6 shadow-sm">
              <div className="flex items-center gap-3 text-gray-800">
                <span className="text-xl font-semibold">${formatCurrency(budget)}</span>
              </div>
            </div>
          </div>

          {/* Predicted card (green) */}
          <Link href="/home/breakdown/cost">
            <div>
              <h3 className="mb-3 text-center text-lg font-medium text-green-600">Predicted</h3>
              <div className="rounded-xl border border-green-200 bg-green-200/70 p-6 shadow-sm">
                <div className="flex items-start gap-3 text-green-900">
                  <div className="leading-6">
                    <div className="text-xl font-semibold">${formatCurrency(predCost)}</div>
                    <div className="text-sm">{percentageCostBeyondBudget.toFixed(1)}% { predCost < budget ? "below" : "beyond" } budget</div>
                    <div className="text-sm">{costBeyondBudget > 0 ? "+" : "-"} ${formatCurrency(costBeyondBudget)}</div>
                  </div>
                </div>
              </div>
            </div>
          </Link>
        </div>
      </section>
    </main>
  );
}
