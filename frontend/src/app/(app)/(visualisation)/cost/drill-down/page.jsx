import PNLDataView from "@/components/visualisation/PNLDataView";
import { formatCurrency } from "@/utils/currency-utils";
import last12MonthsCostPNLData from "@/mock_data/breakdownPage/cost/GetLast12MonthsCostPNLEntryByBU.json"
import next3MonthsCostPNLData from "@/mock_data/breakdownPage/cost/GetNext3MonthsCostPNLForecastByBU.json";

export default function CostDrillDown() {

  const historicalCostPNLDataKeys = last12MonthsCostPNLData.data.keys; // ordered array of "MM-YYYY" from oldest to newest
  const historicalCostPNLDataEntries = last12MonthsCostPNLData.data.entries; // unordered Objects of CostPNLData Objects with "MM-YYYY" as Key
  const historicalCostPNLDataOrderedList = historicalCostPNLDataKeys.map((date) => {
    return historicalCostPNLDataEntries[date]; // List of 12 PNLData Entry Objects
  }); // Convert to ordered list of Cost PNLData Objects from oldest to newest

  const forecastedCostPNLDataKeys = next3MonthsCostPNLData.data.keys;
  const forecastedCostPNLDataEntries = next3MonthsCostPNLData.data.entries;
  const forecastedCostPNLDataEntriesOrderedList = forecastedCostPNLDataKeys.map((date) => {
    return forecastedCostPNLDataEntries[date]; // List of 3 PNLData Forecast Objects
  });

  // Get most recent Cost PNLData Object
  const latestEntryMonth = historicalCostPNLDataKeys[11];
  const latestEntryPNLData = historicalCostPNLDataOrderedList[11];

  // Get upcoming Cost PNLData Forecast e.g. if latestEntryMonth is Jan, get Feb Cost Forecast
  const upcomingForecastPNLData = forecastedCostPNLDataEntriesOrderedList[0];

  // Get Cost PNLData Names to loop through for costCards creation
  const costPNLDataNames = Object.keys(latestEntryPNLData);

  // Create Objects for costCards to be generated in PNLPNLDataView's StatCard Component
  const costCards = costPNLDataNames.map((name) => {
    const isGrowth = latestEntryPNLData[name] <= upcomingForecastPNLData[name];
    // percentageDelta may be negative if not growth but decline
    const percentageDelta = ((upcomingForecastPNLData[name] - latestEntryPNLData[name]) / latestEntryPNLData[name]) * 100;
    const PNLDataValue = upcomingForecastPNLData[name];

    return {
      title: name,
      lines: [
        { label: "Forecasted", value: `SGD ${formatCurrency(PNLDataValue)}` },
        { label: `Monthly ${isGrowth ? "Growth" : "Decline"}`, value: `${percentageDelta.toFixed(2)}%` }
      ],
      accent: percentageDelta >= 0 ? "green" : (percentageDelta <= -5 ? "red" : "yellow")
    }
  })

  return (
    <PNLDataView
      leftCards={costCards} // Array of objects for StatCard Component
      latestEntryMonth={latestEntryMonth} // Most recent month that has an entry in format "MM-YYYY"
      historicalPNLDataOrderedList={historicalCostPNLDataOrderedList} // Ordered list of historical Cost KPI Objects from oldest to newest
      forecastedPNLDataOrderedList={forecastedCostPNLDataEntriesOrderedList}  // Ordered list of forecast Cost KPI Objects from oldest to newest
      PNLDataNames={costPNLDataNames} // To choose first graph in drill-down view
    />
  );
}