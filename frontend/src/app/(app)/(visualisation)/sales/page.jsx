import KPIView from "@/components/visualisation/KPIView";
import { formatCurrency } from "@/utils/currency-utils";
import latestParameters from "@/mock_data/homePage/GetLatestParametersByEmployeeId.json"
import last12MonthsSalesKPIs from "@/mock_data/homePage/sales/GetLast12MonthsSalesKPIsByBU.json"
import next3MonthsSalesKPIs from "@/mock_data/homePage/sales/GetNext3MonthsSalesForecastByBU.json"

export default function Sales() {

  const targets = latestParameters.data;

  const historicalSalesKPIsKeys = last12MonthsSalesKPIs.data.keys; // ordered array of "MM-YYYY" from oldest to newest
  const historicalSalesKPIsEntries = last12MonthsSalesKPIs.data.entries; // unordered Objects of SalesKPI Objects with "MM-YYYY" as Key
  const historicalSalesKPIsOrderedList = historicalSalesKPIsKeys.map((date) => {
    return historicalSalesKPIsEntries[date]; // List of 12 KPI Entry Objects
  }); // Convert to ordered list of SalesKPI Objects from oldest to newest

  const forecastedSalesKPIsKeys = next3MonthsSalesKPIs.data.keys;
  const forecastedSalesKPIsEntries = next3MonthsSalesKPIs.data.entries;
  const forecastedSalesKPIsEntriesOrderedList = forecastedSalesKPIsKeys.map((date) => {
    return forecastedSalesKPIsEntries[date]; // List of 3 KPI Forecast Objects
  });

  console.log("keys:", forecastedSalesKPIsKeys);
  console.log("entries:", forecastedSalesKPIsEntries);

  // Get most recent Sales KPI Object
  const latestEntryMonth = historicalSalesKPIsKeys[11];
  const latestEntryKPI = historicalSalesKPIsOrderedList[11];

  // Get upcoming Sales KPI Forecast e.g. if latestEntryMonth is Jan, get Feb Sales Forecast
  const upcomingForecastKPI = forecastedSalesKPIsEntriesOrderedList[0];

  

  // Get Sales KPI Names to loop through for salesCards creation
  const salesKPINames = Object.keys(latestEntryKPI);

  // Get sales target directly
  const salesTarget = targets["Sales Target"];

  // Create Objects for salesCards to be generated in KPIView's StatCard Component
  const salesCards = salesKPINames.map((name) => {
    console.log("latest entry:", latestEntryKPI[name]);
    console.log("upcoming forecast:", upcomingForecastKPI[name]);

    const isGrowth = latestEntryKPI[name] <= upcomingForecastKPI[name];
    // percentageDelta may be negative if not growth but decline
    const percentageDelta = ((upcomingForecastKPI[name] - latestEntryKPI[name]) / latestEntryKPI[name]) * 100;
    const KPIValue = upcomingForecastKPI[name] < 1 ? upcomingForecastKPI[name] * 100 : upcomingForecastKPI[name];
    const targetValue = targets[name] < 1 ? targets[name] * 100 : targets[name];

    return {
      title: name,
      lines: [
        { label: "Forecasted", value: `${name === "Sales" ? "SGD" : ""}${formatCurrency(KPIValue)}${name !== "Sales" ? "%" : ""}` },
        { label: "Target", value: `${name === "Sales" ? "SGD" : ""}${formatCurrency(name === "Sales" ? salesTarget : targetValue)}${name !== "Sales" ? "%" : ""}` },
        { label: `Monthly ${isGrowth ? "Growth" : "Decline"}`, value: `${percentageDelta.toFixed(2)}%` }
      ],
      accent: percentageDelta >= 0 ? "green" : (percentageDelta <= -5 ? "red" : "yellow")
    }
  })

  return (
    <KPIView
      leftCards={salesCards} // Array of objects for StatCard Component
      activeTab="Sales" // String value for RangeTab Component
      latestEntryMonth={latestEntryMonth} // Most recent month that has an entry in format "MM-YYYY"
      targets={targets} // Object of latest Target Values
      historicalKPIsOrderedList={historicalSalesKPIsOrderedList} // Ordered list of historical Sales KPI Objects from oldest to newest
      forecastedKPIsOrderedList={forecastedSalesKPIsEntriesOrderedList}  // Ordered list of forecast Sales KPI Objects from oldest to newest
    />
  );
}