import { convertFormattedMonthToInt } from "./time-utils";

// Function takes in a month in format "MM-YYYY" and increments the month by (int) monthsAfter
// E.g. getMonthsAfter("09-2024", 4) returns "01-2025"
export function getMonthsAfter( latestMonth, monthsAfter ) {
  // latestMonth is "MM-YYYY"
  const [monthStr, yearStr] = latestMonth.split("-");
  let month = parseInt(monthStr, 10) - 1; // JS Date month is 0-based
  let year = parseInt(yearStr, 10);

  // Create a date from first of that month
  const date = new Date(year, month, 1);

  // Add the months
  date.setMonth(date.getMonth() + monthsAfter);

  // Format back to "MM-YYYY"
  const newMonth = String(date.getMonth() + 1).padStart(2, "0");
  const newYear = date.getFullYear();

  return `${newMonth}-${newYear}`;
}

// Function takes in a month in format "MM-YYYY" and returns a list of the preceding 12 months and incoming 3 months
// E.g. getMonthsLabels("01-2025") returns ["Jan", "Feb", ..... "Dec", "Jan", "Feb", "March"] for 15 total months
export function getMonthsLabels( latestMonth ) {

  const monthIndex = convertFormattedMonthToInt(latestMonth); // minus 1 since arrays start from 0
  const orderedArrayOfMonths = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  ];

  const labels = [];

  // 
  for (let i = monthIndex - 12; i < monthIndex + 3; i++) {
    const currMonthIndex = (i + 12) % 12; // wrap around with modulo
    labels.push(orderedArrayOfMonths[currMonthIndex]);
  }

  return labels;
}
