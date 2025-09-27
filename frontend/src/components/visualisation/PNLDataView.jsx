
"use client"

import { useState, useEffect } from "react";
import StatCard from "@/components/visualisation/StatCard";
import RangeTabs from "@/components/visualisation/RangeTabs";
import PNLDataChartFrame from "@/components/visualisation/PNLDataChartFrame";
import { getMonthsLabels } from "@/utils/date-utils";

// Theme Mapping for syncing style of parent container with chosen Left Side Card
const THEME_MAP = {
  yellow: { panel: "border-yellow-300 bg-yellow-100", frame: "border-yellow-300" },
  red: { panel: "border-red-300 bg-red-100", frame: "border-red-300" },
  green: { panel: "border-green-400 bg-green-100", frame: "border-green-400" },
};

export default function PNLDataView({
  leftCards,
  latestEntryMonth,
  historicalPNLDataOrderedList,
  forecastedPNLDataOrderedList,
  PNLDataNames
}) {

  const [currentRange, setCurrentRange] = useState("6M");
  const [currentPNLDataName, setCurrentPNLDataName] = useState(PNLDataNames[0]) // First name in list is selected to display graph
  const [chartData, setChartData] = useState([]);

  const combinedPNLDataOrderedList = [...historicalPNLDataOrderedList, ...forecastedPNLDataOrderedList];
  const chartXLabels = getMonthsLabels(latestEntryMonth, currentRange);

  function updateChartData(PNLDataName, orderedListOfPNLDataObjects, strRange) {
    const intRange = parseInt(strRange, 10); // Convert "3M" -> 3, "6M" -> 6, "12M" -> 12 in base 10
    const rangedPNLDataObjects = orderedListOfPNLDataObjects.slice(-(intRange + 3)); // Returns new array from index of intRange to Newest PNLData Object, add 3 to account for the forecast values
    const rangedChartData = rangedPNLDataObjects.map((PNLDataObject, index) => {

      return {
        month: chartXLabels[index + (12 - intRange)],
        Historical: index < intRange ? PNLDataObject[PNLDataName] : null,
        Forecasted: (index >= intRange || index === (intRange - 1)) ? PNLDataObject[PNLDataName] : null
      }
    })

    setCurrentRange(strRange);
    setChartData(rangedChartData);
  }

  // Initial chart data based off activeTab ("Profit"/"Sales"/"Cost")
  useEffect(() => {
    updateChartData(currentPNLDataName, combinedPNLDataOrderedList, currentRange);
  }, []);

  // Click handler for cards
  function handleSelectCard(card) {
    const pnlDataKey = card.title;

    setCurrentPNLDataName(pnlDataKey);
    updateChartData(pnlDataKey, combinedPNLDataOrderedList, currentRange);
  }

  // Handle style of parent container containing graphs and cards
  const currentAccent = leftCards.find(c => c.title === currentPNLDataName)?.accent ?? "yellow";
  const theme = THEME_MAP[currentAccent] ?? THEME_MAP.yellow;

  return (
    <main className="mx-auto max-w-6xl p-4 sm:p-6 space-y-4">

      {/* Main panel */}
      <section className={`rounded-2xl border-4 p-4 sm:p-6 space-y-4 transition-colors ${theme.panel}`}>
        <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
          {/* Left stat rail */}
          <div className="md:col-span-4 lg:col-span-3 space-y-3 pt-8">
            <div
              className={`
                space-y-3
                md:max-h-[480px] md:overflow-y-auto md:pr-2 md:pl-1 pt-3 pb-1
                md:scroll-smooth md:snap-y md:snap-mandatory
                md:overscroll-contain
              `}
            >
              {leftCards.map((card, index) => (
                <StatCard key={index} title={card.title} lines={card.lines} accent={card.accent} active={card.title === currentPNLDataName}
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
                updateChartData(currentPNLDataName, combinedPNLDataOrderedList, newRange)
              }} />
            </div>

            <PNLDataChartFrame
              className={`rounded-2xl border-4 p-4 sm:p-6 space-y-4 transition-colors ${theme.frame} bg-white`}
              chartData={chartData} xLabels={chartXLabels}
            />

          </div>
        </div>
      </section>
    </main>
  );
}
