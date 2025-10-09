
"use client"

import { useState, useEffect } from "react";
import Link from "next/link";
import StatCard from "@/components/visualisation/StatCard";
import RangeTabs from "@/components/visualisation/RangeTabs";
import KPIChartFrame from "@/components/visualisation/KPIChartFrame";
import { getMonthsLabels } from "@/utils/date-utils";
import { toNumber } from "@/utils/number-utils";

// Theme Mapping for syncing style of parent container with chosen Left Side Card
const THEME_MAP = {
  gray: { panel: "border-gray-300 bg-gray-100", frame: "border-gray-300" },
  yellow: { panel: "border-yellow-300 bg-yellow-100", frame: "border-yellow-300" },
  red: { panel: "border-red-300 bg-red-100", frame: "border-red-300" },
  green: { panel: "border-green-400 bg-green-100", frame: "border-green-400" },
};

// Drill Down Mapping of ActiveTab to path
const DRILLDOWN = {
  Sales: "/sales/drill-down",
  Cost: "/cost/drill-down",
};

export default function KPIView({
  leftCards,
  activeTab,
  latestEntryMonth,
  targets,
  historicalKPIsOrderedList,
  forecastedKPIsOrderedList
}) {

  const [currentRange, setCurrentRange] = useState("6M");
  const [currentKPIName, setCurrentKPIName] = useState(activeTab);
  const [currentTargetValue, setCurrentTargetValue] = useState(0);
  const [chartData, setChartData] = useState([]);

  const combinedKPIsOrderedList = [...historicalKPIsOrderedList, ...forecastedKPIsOrderedList];
  const chartXLabels = getMonthsLabels(latestEntryMonth, currentRange);

  function updateChartData(KPIName, orderedListOfKPIObjects, strRange) {
    const intRange = parseInt(strRange, 10); // Convert "3M" -> 3, "6M" -> 6, "12M" -> 12 in base 10
    const rangedKPIObjects = orderedListOfKPIObjects.slice(-(intRange + 3)); // Returns new array from index of intRange to Newest KPI Object, add 3 to account for the forecast values
    const rangedChartData = rangedKPIObjects.map((KPIObject, index) => {

      return {
        month: chartXLabels[index + (12 - intRange)],
        Historical: index < intRange ? (KPIObject[KPIName] < 1 ? KPIObject[KPIName] * 100 : KPIObject[KPIName]) : null,
        Forecasted: (index >= intRange || index === (intRange - 1)) ? (KPIObject[KPIName] < 1 ? KPIObject[KPIName] * 100 : KPIObject[KPIName]) : null
      }
    })

    setCurrentRange(strRange);
    setChartData(rangedChartData);
  }

  // Initial chart data based off activeTab ("Profit"/"Sales"/"Cost")
  useEffect(() => {
    // Wait until we have cards and data
    if (leftCards.length === 0 || combinedKPIsOrderedList.length === 0) return;

    const salesTarget = targets["Sales Target"];
    const costBudget = targets["Cost Budget"];
    const profitTarget = salesTarget - costBudget;

    if (activeTab === "Sales") {
      setCurrentTargetValue(salesTarget);
    } else if (activeTab === "Cost") {
      setCurrentTargetValue(costBudget);
    } else if (activeTab === "Profit") {
      setCurrentTargetValue(profitTarget);
    }

    // Set the current KPI name to the first card (which should be Profit/Cost/Sales)
    const firstCardName = leftCards[0]?.title || activeTab;
    setCurrentKPIName(firstCardName);

    updateChartData(currentKPIName, combinedKPIsOrderedList, currentRange);
  }, [leftCards, targets, historicalKPIsOrderedList, forecastedKPIsOrderedList]);

  // Click handler for cards
  function handleSelectCard(card) {
    const kpiKey = card.title;
    const target = toNumber(card.lines[1].value) < 1 ? toNumber(card.lines[1].value) * 100 : toNumber(card.lines[1].value);

    setCurrentKPIName(kpiKey);
    setCurrentTargetValue(target);
    updateChartData(kpiKey, combinedKPIsOrderedList, currentRange);
  }

  // Handle style of parent container containing graphs and cards
  const currentAccent = leftCards.find(c => c.title === currentKPIName)?.accent ?? "gray";
  const theme = THEME_MAP[currentAccent] ?? THEME_MAP.gray;

  const tabLinks = [
    { href: "/profit", label: "Profit" },
    { href: "/sales", label: "Sales" },
    { href: "/cost", label: "Cost" },
  ];

  return (
    <main className="mx-auto max-w-6xl p-4 sm:p-6 space-y-4">
      {/* Profit/Sales/Cost tabs */}
      <div className="flex items-center gap-3">
        <nav className="inline-flex rounded-md border border-gray-300 bg-white shadow-sm overflow-hidden divide-x divide-gray-300">
          {tabLinks.map((tab) => (
            <Link
              key={tab.href}
              href={tab.href}
              className={`px-4 py-2 text-sm ${tab.label === activeTab ? "bg-gray-500 text-white cursor-default" : "bg-gray-100 hover:bg-gray-50 cursor-pointer"}`}
            >
              {tab.label}
            </Link>
          ))}
        </nav>
      </div>

      {/* Main panel */}
      <section className={`rounded-2xl border-4 p-4 sm:p-6 space-y-4 transition-colors ${theme.panel}`}>
        <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
          {/* Left stat rail */}
          <div className="md:col-span-4 lg:col-span-3 space-y-3">
            <div
              className={`
                space-y-3
                md:max-h-[480px] md:overflow-y-auto md:pr-2 md:pl-1 pt-3 pb-1
                md:scroll-smooth md:snap-y md:snap-mandatory
                md:overscroll-contain
              `}
            >
              {leftCards.map((card, index) => (
                <StatCard key={index} title={card.title} lines={card.lines} accent={card.accent} active={card.title === currentKPIName}
                  onClick={() => handleSelectCard(card)}
                />
              ))}
            </div>
          </div>

          {/* Chart side */}
          <div className="md:col-span-8 lg:col-span-9 space-y-3">
            <div className="flex items-center justify-end">
              {/* 3M/6M/12M tabs */}
              <RangeTabs currentRange={currentRange} onChange={(newRange) => {
                updateChartData(currentKPIName, combinedKPIsOrderedList, newRange)
              }} />
            </div>

            <KPIChartFrame
              className={`rounded-2xl border-4 p-4 sm:p-6 space-y-4 transition-colors ${theme.frame} bg-white`}
              chartData={chartData} chartTargetValue={currentTargetValue} xLabels={chartXLabels}
            />

            {DRILLDOWN[activeTab] && (
              <div className="flex justify-end pt-2">
                <Link
                  href={DRILLDOWN[activeTab]}
                  className="inline-flex items-center gap-2 rounded-md
                    border border-gray-300 px-3 py-1.5 text-sm font-medium
                    bg-gray-100 text-black shadow-sm transition
                    hover:bg-gray-50 hover:shadow
                    focus:outline-none focus:ring-2 focus:ring-gray-300"
                >
                  Drill Down
                </Link>
              </div>
            )}

          </div>
        </div>
      </section>
    </main>
  );
}
