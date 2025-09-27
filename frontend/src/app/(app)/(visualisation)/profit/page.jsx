import KPIView from "@/components/visualisation/KPIView";
import { formatCurrency } from "@/utils/currency-utils";
import latestParameters from "@/mock_data/homePage/GetLatestParametersByEmployeeId.json"
import last12MonthsProfitKPIs from "@/mock_data/homePage/profit/GetLast12MonthsProfitKPIsByBU.json"
import next3MonthsProfitKPIs from "@/mock_data/homePage/profit/GetNext3MonthsProfitForecastByBU.json"

export default function Profit() {

  const targets = latestParameters.data;

  const historicalProfitKPIsKeys = last12MonthsProfitKPIs.data.keys; // ordered array of "MM-YYYY" from oldest to newest
  const historicalProfitKPIsEntries = last12MonthsProfitKPIs.data.entries; // unordered Objects of ProfitKPI Objects with "MM-YYYY" as Key
  const historicalProfitKPIsOrderedList = historicalProfitKPIsKeys.map((date) => {
    return historicalProfitKPIsEntries[date]; // List of 12 KPI Entry Objects
  }); // Convert to ordered list of ProfitKPI Objects from oldest to newest

  const forecastedProfitKPIsKeys = next3MonthsProfitKPIs.data.keys;
  const forecastedProfitKPIsEntries = next3MonthsProfitKPIs.data.entries;
  const forecastedProfitKPIsEntriesOrderedList = forecastedProfitKPIsKeys.map((date) => {
    return forecastedProfitKPIsEntries[date]; // List of 3 KPI Forecast Objects
  });

  // Get most recent Profit KPI Object
  const latestEntryMonth = historicalProfitKPIsKeys[11];
  const latestEntryKPI = historicalProfitKPIsOrderedList[11];

  // Get upcoming Profit KPI Forecast e.g. if latestEntryMonth is Jan, get Feb Profit Forecast
  const upcomingForecastKPI = forecastedProfitKPIsEntriesOrderedList[0];

  // Get Profit KPI Names to loop through for profitCards creation
  const profitKPINames = Object.keys(latestEntryKPI);

  // Calculate Profit target as "Sales Target" - "Cost Budget"
  const profitTarget = targets["Sales Target"] - targets["Cost Budget"];

  // Create Objects for profitCards to be generated in KPIView's StatCard Component
  const profitCards = profitKPINames.map((name) => {
    const isGrowth = latestEntryKPI[name] <= upcomingForecastKPI[name];
    // percentageDelta may be negative if not growth but decline
    const percentageDelta = ((upcomingForecastKPI[name] - latestEntryKPI[name]) / latestEntryKPI[name]) * 100;
    const KPIValue = upcomingForecastKPI[name] < 1 ? upcomingForecastKPI[name] * 100 : upcomingForecastKPI[name];
    const targetValue = targets[name] < 1 ? targets[name] * 100 : targets[name];

    return {
      title: name,
      lines: [
        { label: "Forecasted", value: `${name === "Profit" ? "SGD" : ""}${formatCurrency(KPIValue)}${name !== "Profit" ? "%" : ""}` },
        { label: "Target", value: `${name === "Profit" ? "SGD" : ""}${formatCurrency(name === "Profit" ? profitTarget : targetValue)}${name !== "Profit" ? "%" : ""}` },
        { label: `Monthly ${isGrowth ? "Growth" : "Decline"}`, value: `${percentageDelta.toFixed(2)}%` }
      ],
      accent: percentageDelta >= 0 ? "green" : (percentageDelta <= -5 ? "red" : "yellow")
    }
  })

  return (
    <KPIView
      leftCards={profitCards} // Array of objects for StatCard Component
      activeTab="Profit" // String value for RangeTab Component
      latestEntryMonth={latestEntryMonth} // Most recent month that has an entry in format "MM-YYYY"
      targets={targets} // Object of latest Target Values
      historicalKPIsOrderedList={historicalProfitKPIsOrderedList} // Ordered list of historical Profit KPI Objects from oldest to newest
      forecastedKPIsOrderedList={forecastedProfitKPIsEntriesOrderedList}  // Ordered list of forecast Profit KPI Objects from oldest to newest
    />
  );
}