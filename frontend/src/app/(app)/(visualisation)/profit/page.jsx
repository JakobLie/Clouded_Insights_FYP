"use client";

import KPIView from "@/components/visualisation/KPIView";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { formatCurrency } from "@/utils/currency-utils";

export default function Profit() {

  // Get User Object
  const { user, logout } = useAuth();
  const router = useRouter();

  // Set React Hooks
  const [targets, setTargets] = useState({}); // Most recent Profit targets
  const [historicalProfitKPIsOrderedList, setHistoricalProfitKPIsOrderedList] = useState([]); // 12 months historical
  const [forecastedProfitKPIsOrderedList, setForecastedProfitKPIsOrderedList] = useState([]); // 3 months forecasted
  const [latestEntryMonth, setLatestEntryMonth] = useState("");
  const [profitCards, setProfitCards] = useState([]);

  // UX state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Redirect if not logged in
  useEffect(() => {
    if (!user) {
      router.replace("/login");
    };
  }, [user, router]);

  // Fetch all data once we have a user
  useEffect(() => {
    if (!user) return;

    const ac = new AbortController();

    async function loadAllData() {
      setLoading(true);
      setError(null);

      try {
        // Fetch all three endpoints in parallel
        const [targetsResponse, historicalDataResponse, forecastedDataResponse] = await Promise.all([
          fetch(`http://localhost:5000/parameter/latest/${user.id}`, { signal: ac.signal }),
          fetch(`http://localhost:5000/kpi/profit/${user.business_unit}`, { signal: ac.signal }),
          fetch(`http://localhost:5000/kpi/f_profit/${user.business_unit}`, { signal: ac.signal })
        ]);

        // Check if all responses are OK
        if (!targetsResponse.ok || !historicalDataResponse.ok || !forecastedDataResponse.ok) {
          throw new Error(`HTTP Error!
            \nTargets Data Status: ${targetsResponse.status}
            \nHistorical Data Status: ${historicalDataResponse.status}
            \nForecasted Data Status: ${forecastedDataResponse.status}`
          );
        }

        // Parse all responses
        const targetsData = await targetsResponse.json();
        console.log('Fetched targets data:', targetsData);

        const historicalData = await historicalDataResponse.json();
        console.log('Fetched historical profit kpi data:', historicalData);

        const forecastedData = await forecastedDataResponse.json();
        console.log('Fetched forecasted profit kpi data:', forecastedData);

        // Process targets data
        const processedTargets = targetsData.data;
        setTargets(processedTargets);

        // Process historical data
        const historicalKeys = historicalData.data.keys;
        const historicalEntries = historicalData.data.kpis;
        const historicalOrderedList = historicalKeys.map((date) => historicalEntries[date]);
        setHistoricalProfitKPIsOrderedList(historicalOrderedList);

        // Process forecasted data
        const forecastedKeys = forecastedData.data.keys;
        const forecastedEntries = forecastedData.data.kpis;
        const forecastedOrderedList = forecastedKeys.map((date) => forecastedEntries[date]);
        setForecastedProfitKPIsOrderedList(forecastedOrderedList);

        // Get latest entry details
        const latestMonth = historicalKeys[historicalKeys.length - 1];
        setLatestEntryMonth(latestMonth);

        // Get latest and upcoming KPI data
        const latestEntryKPI = historicalOrderedList[historicalOrderedList.length - 1];
        const upcomingForecastKPI = forecastedOrderedList[0];

        // Calculate profit target
        const profitTarget = processedTargets["Sales Target"] - processedTargets["Cost Budget"];

        // Create profit cards
        const profitKPINames = Object.keys(latestEntryKPI);
        const cards = profitKPINames.map((name) => {
          const isGrowth = latestEntryKPI[name] <= upcomingForecastKPI[name];
          const percentageDelta = ((upcomingForecastKPI[name] - latestEntryKPI[name]) / latestEntryKPI[name]) * 100;
          const KPIValue = upcomingForecastKPI[name] < 1 ? upcomingForecastKPI[name] * 100 : upcomingForecastKPI[name];
          const targetValue = processedTargets[name] < 1 ? processedTargets[name] * 100 : processedTargets[name];

          return {
            title: name,
            lines: [
              { label: "Forecasted", value: `${name === "Profit" ? "SGD" : ""}${formatCurrency(KPIValue)}${name !== "Profit" ? "%" : ""}` },
              { label: "Target", value: `${name === "Profit" ? "SGD" : ""}${formatCurrency(name === "Profit" ? profitTarget : targetValue)}${name !== "Profit" ? "%" : ""}` },
              { label: `Monthly ${isGrowth ? "Growth" : "Decline"}`, value: `${percentageDelta.toFixed(2)}%` }
            ],
            accent: percentageDelta >= 0 ? "green" : (percentageDelta <= -5 ? "red" : "yellow")
          };
        });

        // Sort cards: Profit/Cost first, then red, yellow, green
        const sortedCards = cards.sort((a, b) => {
          // Profit/Cost/Sales always comes first
          if (a.title === "Profit") return -1;
          if (b.title === "Profit") return 1;

          // Then sort by accent: red, yellow, green
          const accentOrder = { red: 0, yellow: 1, green: 2, gray: 3 };
          return accentOrder[a.accent] - accentOrder[b.accent];
        });

        setProfitCards(sortedCards);

      } catch (error) {
        if (error.name === 'AbortError') {
          console.log("Fetch aborted");
          return;
        }
        console.error("Error loading parameters:", error);
        setError(error.message);
      } finally {
        setLoading(false)
      }
    }

    loadAllData();

    // Cleanup function to abort fetch if component unmounts
    return () => ac.abort();

  }, [user])


  // Early returns after all hooks
  if (!user) return null;
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-xl text-red-600">Error: {error}</div>
      </div>
    );
  }

  return (
    <KPIView
      leftCards={profitCards} // Array of objects for StatCard Component
      activeTab="Profit" // String value for RangeTab Component
      latestEntryMonth={latestEntryMonth} // Most recent month that has an entry in format "MM-YYYY"
      targets={targets} // Object of latest Target Values
      historicalKPIsOrderedList={historicalProfitKPIsOrderedList} // Ordered list of historical Profit KPI Objects from oldest to newest
      forecastedKPIsOrderedList={forecastedProfitKPIsOrderedList}  // Ordered list of forecast Profit KPI Objects from oldest to newest
    />
  );
}