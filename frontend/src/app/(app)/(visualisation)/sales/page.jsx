"use client"

import KPIView from "@/components/visualisation/KPIView";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { formatCurrency } from "@/utils/currency-utils";

export default function Sales() {

  // Get User Object
  const { user, logout } = useAuth();
  const router = useRouter();

  // Set React Hooks
  const [targets, setTargets] = useState({}); // Most recent Sales targets
  const [historicalSalesKPIsOrderedList, setHistoricalSalesKPIsOrderedList] = useState([]); // 12 months historical
  const [forecastedSalesKPIsOrderedList, setForecastedSalesKPIsOrderedList] = useState([]); // 3 months forecasted
  const [latestEntryMonth, setLatestEntryMonth] = useState("");
  const [salesCards, setSalesCards] = useState([]);

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
          fetch(`http://localhost:5000/kpi/sales/${user.business_unit}`, { signal: ac.signal }),
          fetch(`http://localhost:5000/kpi/f_sales/${user.business_unit}`, { signal: ac.signal })
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
        console.log('Fetched historical sales kpi data:', historicalData);

        const forecastedData = await forecastedDataResponse.json();
        console.log('Fetched forecasted sales kpi data:', forecastedData);

        // Process targets data
        const processedTargets = targetsData.data;
        setTargets(processedTargets);

        // Process historical data
        const historicalKeys = historicalData.data.keys;
        const historicalEntries = historicalData.data.kpis;
        const historicalOrderedList = historicalKeys.map((date) => historicalEntries[date]);
        setHistoricalSalesKPIsOrderedList(historicalOrderedList);

        // Process forecasted data
        const forecastedKeys = forecastedData.data.keys;
        const forecastedEntries = forecastedData.data.kpis;
        const forecastedOrderedList = forecastedKeys.map((date) => forecastedEntries[date]);
        setForecastedSalesKPIsOrderedList(forecastedOrderedList);

        // Get latest entry details
        const latestMonth = historicalKeys[historicalKeys.length - 1];
        setLatestEntryMonth(latestMonth);

        // Get latest and upcoming KPI data
        const latestEntryKPI = historicalOrderedList[historicalOrderedList.length - 1];
        const upcomingForecastKPI = forecastedOrderedList[0];

        // Calculate sales target
        const salesTarget = processedTargets["Sales Target"];

        // Create sales cards
        const salesKPINames = Object.keys(latestEntryKPI);
        const cards = salesKPINames.map((name) => {
          const isGrowth = latestEntryKPI[name] <= upcomingForecastKPI[name];
          const percentageDelta = ((upcomingForecastKPI[name] - latestEntryKPI[name]) / latestEntryKPI[name]) * 100;
          const KPIValue = upcomingForecastKPI[name] < 1 ? upcomingForecastKPI[name] * 100 : upcomingForecastKPI[name];
          const targetValue = processedTargets[name] < 1 ? processedTargets[name] * 100 : processedTargets[name];

          return {
            title: name,
            lines: [
              { label: "Forecasted", value: `${name === "Sales" ? "SGD" : ""}${formatCurrency(KPIValue)}${name !== "Sales" ? "%" : ""}` },
              { label: "Target", value: `${name === "Sales" ? "SGD" : ""}${formatCurrency(name === "Sales" ? salesTarget : targetValue)}${name !== "Sales" ? "%" : ""}` },
              { label: `Monthly ${isGrowth ? "Growth" : "Decline"}`, value: `${percentageDelta.toFixed(2)}%` }
            ],
            accent: percentageDelta >= 0 ? "green" : (percentageDelta <= -5 ? "red" : "yellow")
          };
        });

        // Sort cards: Profit/Cost first, then red, yellow, green
        const sortedCards = cards.sort((a, b) => {
          // Profit/Cost always comes first
          if (a.title === "Profit") return -1;
          if (b.title === "Profit") return 1;

          // Then sort by accent: red, yellow, green
          const accentOrder = { red: 0, yellow: 1, green: 2, gray: 3 };
          return accentOrder[a.accent] - accentOrder[b.accent];
        });

        setSalesCards(sortedCards);

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
      leftCards={salesCards} // Array of objects for StatCard Component
      activeTab="Sales" // String value for RangeTab Component
      latestEntryMonth={latestEntryMonth} // Most recent month that has an entry in format "MM-YYYY"
      targets={targets} // Object of latest Target Values
      historicalKPIsOrderedList={historicalSalesKPIsOrderedList} // Ordered list of historical Sales KPI Objects from oldest to newest
      forecastedKPIsOrderedList={forecastedSalesKPIsOrderedList}  // Ordered list of forecast Sales KPI Objects from oldest to newest
    />
  );
}