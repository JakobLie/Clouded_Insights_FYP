import PNLDataView from "@/components/visualisation/PNLDataView";
import { formatCurrency } from "@/utils/currency-utils";
import last12MonthsSalesPNLData from "@/mock_data/breakdownPage/sales/GetLast12MonthsSalesPNLEntryByBU.json"
import next3MonthsSalesPNLData from "@/mock_data/breakdownPage/sales/GetNext3MonthsSalesPNLForecastByBU.json";

export default function SalesDrillDown() {

  const historicalSalesPNLDataKeys = last12MonthsSalesPNLData.data.keys; // ordered array of "MM-YYYY" from oldest to newest
  const historicalSalesPNLDataEntries = last12MonthsSalesPNLData.data.entries; // unordered Objects of SalesPNLData Objects with "MM-YYYY" as Key
  const historicalSalesPNLDataOrderedList = historicalSalesPNLDataKeys.map((date) => {
    return historicalSalesPNLDataEntries[date]; // List of 12 PNLData Entry Objects
  }); // Convert to ordered list of Sales PNLData Objects from oldest to newest

  const forecastedSalesPNLDataKeys = next3MonthsSalesPNLData.data.keys;
  const forecastedSalesPNLDataEntries = next3MonthsSalesPNLData.data.entries;
  const forecastedSalesPNLDataEntriesOrderedList = forecastedSalesPNLDataKeys.map((date) => {
    return forecastedSalesPNLDataEntries[date]; // List of 3 PNLData Forecast Objects
  });

  // Get most recent Sales PNLData Object
  const latestEntryMonth = historicalSalesPNLDataKeys[11];
  const latestEntryPNLData = historicalSalesPNLDataOrderedList[11];

  // Get upcoming Sales PNLData Forecast e.g. if latestEntryMonth is Jan, get Feb Sales Forecast
  const upcomingForecastPNLData = forecastedSalesPNLDataEntriesOrderedList[0];

  // Get Sales PNLData Names to loop through for SalesCards creation
  const salesPNLDataNames = Object.keys(latestEntryPNLData);

  // Create Objects for SalesCards to be generated in PNLPNLDataView's StatCard Component
  const salesCards = salesPNLDataNames.map((name) => {
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
          leftCards={salesCards} // Array of objects for StatCard Component
          latestEntryMonth={latestEntryMonth} // Most recent month that has an entry in format "MM-YYYY"
          historicalPNLDataOrderedList={historicalSalesPNLDataOrderedList} // Ordered list of historical Sales KPI Objects from oldest to newest
          forecastedPNLDataOrderedList={forecastedSalesPNLDataEntriesOrderedList}  // Ordered list of forecast Sales KPI Objects from oldest to newest
          PNLDataNames={salesPNLDataNames} // To choose first graph in drill-down view
        />
  );
}