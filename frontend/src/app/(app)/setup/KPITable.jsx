import { useState, useEffect } from "react";
import { getCurrentDateFormatted } from "@/utils/time-utils";

export default function KPITable({ defaultKPIValues, pastTargetsOrderedList, onChange }) {

  // before: const KPI_KEYS = Object.keys(defaultKPIValues || {});
  const EXCLUDE = new Set(["Sales Target", "Cost Budget", "Input Date"]);
  const KPI_KEYS = Object.keys(defaultKPIValues || {}).filter(k => !EXCLUDE.has(k));

  // // Form state for ALL targets
  // const [targetFormData, setTargetsFormData] = useState({});

  // test funcrtion to see if API reqs to backend function properly
  // function PushButton() {
  //   // Example: POST request with fetch
  //   fetch("http://localhost:5000/parameter/batch/", {
  //     method: "POST", // HTTP method
  //     headers: {
  //       "Content-Type": "application/json" // tell server we're sending JSON
  //     },
  //     body: JSON.stringify({
  //       "employee_id": "abcd-abcd-abcd",
  //       "parameters": {
  //         "Net Profit Margin": 0.15,
  //         "Receivables Turnover": 0.40,
  //         "Cost Budget": 23100,
  //         "New Target": 21.33,
  //         "New Target 2": 0.55,
  //         "New Target 3": 1010,
  //         "NEW TARGET !@#$": 123456789.12345
  //       }
  //     }) // request body must be a string (e.g. JSON.stringify for JSON)
  //   })
  //     .then(response => {
  //       if (!response.ok) {
  //         throw new Error("Network response was not ok " + response.statusText);
  //       }
  //       return response.json(); // parse JSON response
  //     })
  //     .then(data => {
  //       console.log("Success:", data);
  //     })
  //     .catch(error => {
  //       console.error("Error:", error);
  //     });
  // }



  // Local input state (user is editing a NEW row), initialise with default/latest targets
  const [salesTarget, setSalesTarget] = useState(defaultKPIValues["Sales Target"]);
  const [costBudget, setCostBudget] = useState(defaultKPIValues["Cost Budget"]);
  const [grossProfitMargin, setGrossProfitMargin] = useState(defaultKPIValues["Gross Profit Margin"]);
  const [operatingProfitMargin, setOperatingProfitMargin] = useState(defaultKPIValues["Operating Profit Margin"]);
  const [netProfitMargin, setNetProfitMargin] = useState(defaultKPIValues["Net Profit Margin"]);
  const [quickRatio, setQuickRatio] = useState(defaultKPIValues["Quick Ratio"]);
  const [returnOnSales, setReturnOnSales] = useState(defaultKPIValues["Return On Sales"]);
  const [daysSalesOutstanding, setDaysSalesOutstanding] = useState(defaultKPIValues["Days Sales Outstanding"]);
  const [receivablesTurnover, setReceivablesTurnover] = useState(defaultKPIValues["Receivables Turnover"]);
  const [costOfGoodsSoldRatio, setCostOfGoodsSoldRatio] = useState(defaultKPIValues["Cost Of Goods Sold Ratio"]);
  const [daysPayableOutstanding, setDaysPayableOutstanding] = useState(defaultKPIValues["Days Payable Outstanding"]);
  const [overheadRatio, setOverheadRatio] = useState(defaultKPIValues["Overhead Ratio"]);

  // ---- Initialize KPI inputs from defaults (decimals -> whole % strings)
  useEffect(() => {
    const toPercentInt = (k) =>
      Number.isFinite(defaultKPIValues[k]) ? String(Math.round(defaultKPIValues[k] * 100)) : "";

    setSalesTarget(String(defaultKPIValues["Sales Target"] ?? ""));
    setCostBudget(String(defaultKPIValues["Cost Budget"] ?? ""));

    setGrossProfitMargin(toPercentInt("Gross Profit Margin"));
    setOperatingProfitMargin(toPercentInt("Operating Profit Margin"));
    setNetProfitMargin(toPercentInt("Net Profit Margin"));
    setQuickRatio(toPercentInt("Quick Ratio"));
    setReturnOnSales(toPercentInt("Return On Sales"));
    setDaysSalesOutstanding(toPercentInt("Days Sales Outstanding"));
    setReceivablesTurnover(toPercentInt("Receivables Turnover"));
    setCostOfGoodsSoldRatio(toPercentInt("Cost Of Goods Sold Ratio"));
    setDaysPayableOutstanding(toPercentInt("Days Payable Outstanding"));
    setOverheadRatio(toPercentInt("Overhead Ratio"));
  }, [defaultKPIValues]);

  // ---- Lookup so we can `.map` while using separate states
  const kpiState = {
    "Gross Profit Margin": [grossProfitMargin, setGrossProfitMargin],
    "Operating Profit Margin": [operatingProfitMargin, setOperatingProfitMargin],
    "Net Profit Margin": [netProfitMargin, setNetProfitMargin],
    "Quick Ratio": [quickRatio, setQuickRatio],
    "Return On Sales": [returnOnSales, setReturnOnSales],
    "Days Sales Outstanding": [daysSalesOutstanding, setDaysSalesOutstanding],
    "Receivables Turnover": [receivablesTurnover, setReceivablesTurnover],
    "Cost Of Goods Sold Ratio": [costOfGoodsSoldRatio, setCostOfGoodsSoldRatio],
    "Days Payable Outstanding": [daysPayableOutstanding, setDaysPayableOutstanding],
    "Overhead Ratio": [overheadRatio, setOverheadRatio],
  };

  // ---- Helpers to build a single payload for the parent
  const toNumber = (v) => {
    const n = Number(String(v ?? "").replace(/[^\d.-]/g, ""));
    return Number.isFinite(n) ? n : 0;
  };

  const buildPayload = (overrides = {}) => {
    // Read current values (overrides take precedence)
    const readStr = (cur, key) => String(overrides[key] ?? cur ?? "");
    const payload = {
      "Sales Target": toNumber(readStr(salesTarget, "Sales Target")),
      "Cost Budget": toNumber(readStr(costBudget, "Cost Budget")),
      "Input Date": getCurrentDateFormatted(),
    };
    // KPIs: convert whole % back to decimals
    for (const name of KPI_KEYS) {
      const [val] = kpiState[name] || [""];
      payload[name] = toNumber(readStr(val, name)) / 100;
    }
    return payload;
  };

  // One-liner to set state + notify parent (if provided)
  const setAndEmit = (setter, keyForPayload) => (v) => {
    setter(v);
    onChange && onChange(buildPayload({ [keyForPayload]: v }));
  };

  return (
    <section className="rounded-xl">
      {/* Scroll container */}
      <div className="overflow-x-auto rounded-xl">
        {/* <button onClick={PushButton}>
          PUSH ME
        </button> */}

        <table className="min-w-max w-full text-sm ">
          {/* Sticky header */}
          <thead className="bg-slate-600 text-white sticky top-0 ">
            <tr className="[&>th]:px-4 [&>th]:py-3 [&>th]:font-semibold ">
              <th className="text-center whitespace-nowrap">Sales target (SGD)</th>
              <th className="text-center whitespace-nowrap">Cost budget (SGD)</th>

              {KPI_KEYS.map((KPIName) => (
                <th key={KPIName} className="text-center whitespace-nowrap">
                  {KPIName} (%)
                </th>
              ))}

              <th className="text-left whitespace-nowrap">Input Date</th>
            </tr>
          </thead>



          <tbody className="[&>tr>td]:px-4 [&>tr>td]:py-3 text-center">
            {/* Input row */}
            <tr className="align-middle">
              <td>
                <input
                  type="number"
                  inputMode="decimal"
                  className="h-10 rounded-md bg-gray-200 px-1 py-2 text-center pl-5 font-semibold"
                  value={salesTarget ?? ""}
                  onChange={(e) => setAndEmit(setSalesTarget, "Sales Target")(e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  inputMode="decimal"
                  className="h-10 rounded-md bg-gray-200 px-1 py-2 text-center pl-5 font-semibold"
                  value={costBudget ?? ""}
                  onChange={(e) => setAndEmit(setCostBudget, "Cost Budget")(e.target.value)}
                />
              </td>

              {KPI_KEYS.map((KPIName) => {
                const [val, setVal] = kpiState[KPIName] || ["", () => { }];
                return (
                  <td key={KPIName} >
                    <input
                      type="number"
                      inputMode="decimal"
                      className="h-10 rounded-md bg-gray-200 px-1 py-2 text-center pl-5 font-semibold"
                      value={val ?? ""}
                      onChange={(e) => setAndEmit(setVal, KPIName)(e.target.value)}
                    />
                  </td>
                );
              }
              )}

              <td className="whitespace-nowrap">{getCurrentDateFormatted()}</td>
            </tr>

            {/* Historical rows */}
            {(pastTargetsOrderedList || []).map((parameterObject) => (
              <tr key={parameterObject["Input Date"]} className="border-t">
                <td className="whitespace-nowrap">
                  {parameterObject["Sales Target"] ?? "—"}
                </td>
                <td className="whitespace-nowrap">
                  {parameterObject["Cost Budget"] ?? "—"}
                </td>

                {KPI_KEYS.map((KPIName) => (
                  <td key={`${parameterObject["Input Date"]}-${KPIName}`} className="whitespace-nowrap">
                    {parameterObject[KPIName] !== undefined ? `${(parameterObject[KPIName] * 100).toFixed(0)}` : "—"}
                  </td>
                ))}

                <td className="whitespace-nowrap">{parameterObject["Input Date"]}</td>
              </tr>
            ))}

          </tbody>
        </table>
      </div>
    </section >
  );
}