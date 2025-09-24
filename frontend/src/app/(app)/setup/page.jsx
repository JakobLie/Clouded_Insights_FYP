"use client"

import Image from "next/image";
import { useState, useEffect, useMemo } from "react";
import KPITable from "./KPITable";
import parametersData from "../../../mock_data/setupPage/GetAllParametersByEmployeeId.json";
import employeeData from "../../../mock_data/setupPage/GetEmployeeByEmployeeId.json";

export default function Setup() {

  const [ employeeDetails, setEmployeeDetails] = useState({});
  const [ pastTargets, setPastTargets ] = useState([]);
  const [ newTargets, setNewTargets ] = useState(null);
  const [ saving, setSaving ] = useState(false);

  const pastTargetsKeys = parametersData.data.keys; // ordered array of "MM-YYYY" from oldest to newest
  const pastTargetsEntries = parametersData.data.entries; // unordered Objects of Parameter Objects with "MM-YYYY" as Key
  const pastTargetsOrderedList = pastTargetsKeys.map((date) => {
    return pastTargetsEntries[date]; // List of Parameter Objects
  }).reverse(); // Convert to ordered list of Paramter Objects from newest to oldest (using reverse())

  useEffect(() => {
    setEmployeeDetails(employeeData.data);
    setPastTargets(pastTargetsOrderedList);
  }, []); // Run once intially only

  // Init default KPI values if no historical, else use latest KPIs
  const fallbackDefaults = {
  "Gross Profit Margin": 0.53,
  "Operating Profit Margin": 0.42,
  "Net Profit Margin": 0.31,
  "Quick Ratio": 0.33,
  "Return On Sales": 0.24,
  "Days Sales Outstanding": 0.42,
  "Receivables Turnover": 0.55,
  "Cost Of Goods Sold Ratio": 0.66,
  "Days Payable Outstanding": 0.47,
  "Overhead Ratio": 0.39,
};

const defaultKPIValues = useMemo(() => {
  if (!pastTargets || pastTargets.length === 0) return fallbackDefaults;

  // pick the latest row (adjust if your ordering is oldest->newest)
  const latest = pastTargets[0]; // or pastTargets.at(-1)
  const { ["Input Date"]: _omit, ...rest } = latest; // drop date
  return rest;
}, [pastTargets]);

  // Ensure the payload has an Input Date; use today if missing
  const withInputDate = (obj) => ({
    "Input Date": obj?.["Input Date"] || getCurrentDateFormatted(),
    ...obj,
  });

  /* TO ADJUST FOR API CALL */
  // Update DB with new Targets 
  const handleUpdate = async () => {
    if (!newTargets) return;
    setSaving(true);

    const newRow = withInputDate(newTargets);

    // 1) Mock: update UI immediately (prepend newest)
    setPastTargets(prev => [newRow, ...prev]);

    // 2) (Optional) POST to your API
    try {
      // const res = await fetch("/api/targets", {
      //   method: "POST",
      //   headers: { "Content-Type": "application/json" },
      //   body: JSON.stringify({
      //     employeeId: employeeDetails.id,
      //     parameters: newRow,
      //   }),
      // });
      // if (!res.ok) throw new Error("Failed to save targets");
    } catch (err) {
      console.error(err);
      // Optionally rollback the optimistic add:
      // setPastTargets(prev => prev.filter(r => r !== newRow));
    } finally {
      setSaving(false);
    }
  };


  return (
    <main className="mx-auto max-w-5xl p-6 space-y-6">
      {/* Header card */}
      <section className="rounded-2xl bg-gray-200 p-6 shadow-sm">
        <div className="flex items-center justify-between border-b border-gray-300 pb-3">
          <div className="text-sm font-semibold text-white">
            <span className="rounded-lg bg-slate-600 px-3 py-1">Employee ID: {employeeDetails.id}</span>
          </div>
        </div>

        <div className="mt-5 grid grid-cols-1 gap-6 md:grid-cols-3">
          {/* Avatar + Name */}
          <div className="col-span-2 flex items-center gap-4">
            {/* Profile Image Placeholder */}
                    <div style={{
                      border: '3px solid gray',
                      borderRadius: '50%',
                      overflow: 'hidden'
                    }}>
                      <Image
                        src={"/profile-pic.jpg"}
                        height={110}
                        width={110}
                        alt="profile picture"
                      />
                    </div>
            <div className="space-y-1">
              <h1 className="text-3xl font-extrabold leading-tight">{employeeDetails.name}</h1>
            </div>
          </div>

          {/* Job info */}
          <div className="md:text-right">
            <div className="text-xl font-bold">Job Title:</div>
            <div className="text-xl">{employeeDetails.role}</div>
            <div className="mt-2 text-xl font-bold">Business Unit(s):</div>
            <div className="text-xl">{employeeDetails.business_unit}</div>
          </div>
        </div>
      </section>

      {/* Columns header (tabs look) */}
      <KPITable defaultKPIValues={defaultKPIValues} pastTargetsOrderedList={pastTargets} onChange={setNewTargets} />

      {/* Footer actions */}
      <div className="flex justify-end">
        <button
          className="rounded-xl bg-indigo-700 px-6 py-3 text-xl font-extrabold text-white cursor-pointer"
          onClick={handleUpdate}
          disabled={saving || !newTargets}
        >
          {saving ? "Updating..." : "Update"}
        </button>
      </div>
    </main>
  );
}