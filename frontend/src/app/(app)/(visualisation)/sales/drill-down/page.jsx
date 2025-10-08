"use client"

import PNLDataView from "@/components/visualisation/PNLDataView";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import { formatCurrency } from "@/utils/currency-utils";

export default function SalesDrillDown() {

  // Get User Object
  const { user, logout } = useAuth();
  const router = useRouter();

  // Set React Hooks
  const [historicalSalesPNLOrderedList, setHistoricalSalesPNLOrderedList] = useState([]); // 12 months historical
  const [forecastedSalesPNLOrderedList, setForecastedSalesPNLOrderedList] = useState([]); // 3 months forecasted
  const [latestEntryMonth, setLatestEntryMonth] = useState("");
  const [salesCards, setSalesCards] = useState([]);
  const [salesPNLNames, setSalesPNLNames] = useState([]);

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
          fetch(`http://localhost:5000/entry/sales/${user.business_unit}`, { signal: ac.signal }),
          fetch(`http://localhost:5000/forecast/sales/${user.business_unit}`, { signal: ac.signal })
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

        // Process historical data
        const historicalKeys = historicalData.data.keys;
        const historicalEntries = historicalData.data.entries;
        const historicalOrderedList = historicalKeys.map((date) => historicalEntries[date]);
        setHistoricalSalesPNLOrderedList(historicalOrderedList);

        // Process forecasted data
        const forecastedKeys = forecastedData.data.keys;
        const forecastedEntries = forecastedData.data.forecasts;
        const forecastedOrderedList = forecastedKeys.map((date) => forecastedEntries[date]);
        setForecastedSalesPNLOrderedList(forecastedOrderedList);

        // Get latest entry details
        const latestMonth = historicalKeys[historicalKeys.length - 1];
        setLatestEntryMonth(latestMonth);

        // Get latest and upcoming PNL data
        const latestEntryPNL = historicalOrderedList[historicalOrderedList.length - 1];
        const upcomingForecastPNL = forecastedOrderedList[0];

        // Create sales cards
        const salesPNLNames = Object.keys(latestEntryPNL);
        setSalesPNLNames(salesPNLNames)
        const cards = salesPNLNames.map((name) => {
          const isGrowth = latestEntryPNL[name] <= upcomingForecastPNL[name];
          const percentageDelta = ((upcomingForecastPNL[name] - latestEntryPNL[name]) / latestEntryPNL[name]) * 100;
          const PNLValue = upcomingForecastPNL[name] < 1 ? upcomingForecastPNL[name] * 100 : upcomingForecastPNL[name];

          return {
            title: name,
            lines: [
              { label: "Forecasted", value: `${name === "Sales" ? "SGD" : ""}${formatCurrency(PNLValue)}${name !== "Sales" ? "%" : ""}` },
              { label: `Monthly ${isGrowth ? "Growth" : "Decline"}`, value: `${percentageDelta.toFixed(2)}%` }
            ],
            accent: isNaN(percentageDelta) ? "gray" : (percentageDelta >= 0 ? "green" : (percentageDelta <= -5 ? "red" : "yellow"))
          };
        });

        setSalesCards(cards);

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
    <PNLDataView
      leftCards={salesCards} // Array of objects for StatCard Component
      latestEntryMonth={latestEntryMonth} // Most recent month that has an entry in format "MM-YYYY"
      historicalPNLDataOrderedList={historicalSalesPNLOrderedList} // Ordered list of historical Sales KPI Objects from oldest to newest
      forecastedPNLDataOrderedList={forecastedSalesPNLOrderedList}  // Ordered list of forecast Sales KPI Objects from oldest to newest
      PNLDataNames={salesPNLNames} // To choose first graph in drill-down view
    />
  );
}