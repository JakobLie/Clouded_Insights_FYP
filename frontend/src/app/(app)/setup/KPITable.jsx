import { useState, useEffect } from "react";
import { getCurrentDateFormatted } from "@/utils/time-utils";

export default function KPITable({ defaultKPIValues, pastTargetsOrderedList, onChange }) {

  const EXCLUDE = new Set(["SALES", "COST", "Input Date"]);
  const KPI_KEYS = Object.keys(defaultKPIValues || {}).filter(k => !EXCLUDE.has(k));

  // Single state object for the entire form
  const [formData, setFormData] = useState({});

  // Initialize form data from defaults
  useEffect(() => {
    const initialData = {
      "SALES": defaultKPIValues["SALES"] ?? "",
      "COST": defaultKPIValues["COST"] ?? "",
    };

    // Convert decimal KPIs to whole percentages for display
    KPI_KEYS.forEach(key => {
      const value = defaultKPIValues[key];
      initialData[key] = Number.isFinite(value) ? Math.round(value * 100) : "";
    });

    setFormData(initialData);
  }, [defaultKPIValues]);

  // Single change handler for all inputs
  const handleInputChange = (fieldName, value) => {
    const updatedData = {
      ...formData,
      [fieldName]: value
    };
    setFormData(updatedData);

    // Notify parent with converted values (percentages back to decimals)
    if (onChange) {
      const payload = buildPayloadFromForm(updatedData);
      onChange(payload);
    }
  };

  // Convert form data to API format
  const buildPayloadFromForm = (data) => {
    const toNumber = (v) => {
      const n = Number(String(v ?? "").replace(/[^\d.-]/g, ""));
      return Number.isFinite(n) ? n : 0;
    };

    const payload = {
      "SALES": toNumber(data["SALES"]),
      "COST": toNumber(data["COST"]),
    };

    // Convert percentage inputs back to decimals for KPIs
    KPI_KEYS.forEach(key => {
      payload[key] = toNumber(data[key]) / 100;
    });

    return payload;
  };

  return (
    <section className="rounded-xl">
      {/* Scroll container */}
      <div className="overflow-x-auto rounded-xl">
        <table className="min-w-max w-full text-sm ">
          {/* Sticky header */}
          <thead className="bg-slate-600 text-white sticky top-0 ">
            <tr className="[&>th]:px-4 [&>th]:py-3 [&>th]:font-semibold ">
              <th className="text-center whitespace-nowrap">SALES (SGD)</th>
              <th className="text-center whitespace-nowrap">COST (SGD)</th>

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
                  value={formData["SALES"] ?? ""}
                  onChange={(e) => handleInputChange("SALES", e.target.value)}
                />
              </td>
              <td>
                <input
                  type="number"
                  inputMode="decimal"
                  className="h-10 rounded-md bg-gray-200 px-1 py-2 text-center pl-5 font-semibold"
                  value={formData["COST"] ?? ""}
                  onChange={(e) => handleInputChange("COST", e.target.value)}
                />
              </td>

              {KPI_KEYS.map((KPIName) => {
                return (
                  <td key={KPIName} >
                    <input
                      type="number"
                      inputMode="decimal"
                      className="h-10 rounded-md bg-gray-200 px-1 py-2 text-center pl-5 font-semibold"
                      value={formData[KPIName] ?? ""}
                      onChange={(e) => handleInputChange(KPIName, e.target.value)}
                    />
                  </td>
                );
              }
              )}

              <td className="whitespace-nowrap">{getCurrentDateFormatted()}</td>
            </tr>

            {/* Historical rows */}
            {(pastTargetsOrderedList || []).map((parameterObject, index) => (
              <tr key={parameterObject["Input Date"] || index} className="border-t">
                <td className="whitespace-nowrap">
                  {parameterObject["SALES"] ?? "—"}
                </td>
                <td className="whitespace-nowrap">
                  {parameterObject["COST"] ?? "—"}
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