import KPIView from "@/components/visualisation/KPIView";
import { formatCurrency } from "@/utils/currency-utils";
import latestParameters from "@/mock_data/homePage/GetLatestParametersByEmployeeId.json"
import last12MonthsCostKPIs from "@/mock_data/homePage/cost/GetLast12MonthsCostKPIsByBU.json"
import next3MonthsCostKPIs from "@/mock_data/homePage/cost/GetNext3MonthsCostForecastByBU.json"

export default function Cost() {

  const targets = latestParameters.data;

  const historicalCostKPIsKeys = last12MonthsCostKPIs.data.keys; // ordered array of "MM-YYYY" from oldest to newest
  const historicalCostKPIsEntries = last12MonthsCostKPIs.data.entries; // unordered Objects of CostKPI Objects with "MM-YYYY" as Key
  const historicalCostKPIsOrderedList = historicalCostKPIsKeys.map((date) => {
    return historicalCostKPIsEntries[date]; // List of 12 KPI Entry Objects
  }); // Convert to ordered list of CostKPI Objects from oldest to newest

  const forecastedCostKPIsKeys = next3MonthsCostKPIs.data.keys;
  const forecastedCostKPIsEntries = next3MonthsCostKPIs.data.entries;
  const forecastedCostKPIsEntriesOrderedList = forecastedCostKPIsKeys.map((date) => {
    return forecastedCostKPIsEntries[date]; // List of 3 KPI Forecast Objects
  });

  // Get most recent Cost KPI Object
  const latestEntryMonth = historicalCostKPIsKeys[11];
  const latestEntryKPI = historicalCostKPIsOrderedList[11];

  // Get upcoming Cost KPI Forecast e.g. if latestEntryMonth is Jan, get Feb Cost Forecast
  const upcomingForecastKPI = forecastedCostKPIsEntriesOrderedList[0];

  // Get Cost KPI Names to loop through for costCards creation
  const costKPINames = Object.keys(latestEntryKPI);

  // Get cost target directly
  const costTarget = targets["Cost Budget"];

  // Create Objects for costCards to be generated in KPIView's StatCard Component
  const costCards = costKPINames.map((name) => {
    const isGrowth = latestEntryKPI[name] <= upcomingForecastKPI[name];
    // percentageDelta may be negative if not growth but decline
    const percentageDelta = ((upcomingForecastKPI[name] - latestEntryKPI[name]) / latestEntryKPI[name]) * 100;
    const KPIValue = upcomingForecastKPI[name] < 1 ? upcomingForecastKPI[name] * 100 : upcomingForecastKPI[name];
    const targetValue = targets[name] < 1 ? targets[name] * 100 : targets[name];

    return {
      title: name,
      lines: [
        { label: "Forecasted", value: `${name === "Cost" ? "SGD" : ""}${formatCurrency(KPIValue)}${name !== "Cost" ? "%" : ""}` },
        { label: "Target", value: `${name === "Cost" ? "SGD" : ""}${formatCurrency(name === "Cost" ? costTarget : targetValue)}${name !== "Cost" ? "%" : ""}` },
        { label: `Monthly ${isGrowth ? "Growth" : "Decline"}`, value: `${percentageDelta.toFixed(2)}%` }
      ],
      accent: percentageDelta >= 0 ? "green" : (percentageDelta <= -5 ? "red" : "yellow")
    }
  })

  return (
    <KPIView
      leftCards={costCards} // Array of objects for StatCard Component
      activeTab="Cost" // String value for RangeTab Component
      latestEntryMonth={latestEntryMonth} // Most recent month that has an entry in format "MM-YYYY"
      targets={targets} // Object of latest Target Values
      historicalKPIsOrderedList={historicalCostKPIsOrderedList} // Ordered list of historical Cost KPI Objects from oldest to newest
      forecastedKPIsOrderedList={forecastedCostKPIsEntriesOrderedList}  // Ordered list of forecast Cost KPI Objects from oldest to newest
    />
  );
}