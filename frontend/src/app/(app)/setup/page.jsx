"use client"

import Image from "next/image";
import { useState, useEffect, useMemo } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import KPITable from "./KPITable";
import FileUploadModal from "./FileUploadModal";
import { getCurrentDateFormatted } from "@/utils/time-utils";

export default function Setup() {

  // Get User Object
  const { user, logout } = useAuth();
  const router = useRouter();

  // Set React Hooks
  const [employeeDetails, setEmployeeDetails] = useState({});
  const [pastTargets, setPastTargets] = useState([]);
  const [newTargets, setNewTargets] = useState(null);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false); // Add modal state


  // UX state
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  // Redirect if not logged in
  useEffect(() => {
    if (!user) {
      router.replace("/login");
    };
  }, [user, router]);

  // Fetch parameters once we have a user
  useEffect(() => {
    if (!user) return;

    const ac = new AbortController();

    async function loadParameters() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(`http://localhost:5000/parameter/all/${user.id}/`,
          { signal: ac.signal }
        );

        if (!response.ok) {
          throw new Error(`HTTP Error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Fetched parameters data:', data);

        // Process the parameters data
        const pastTargetsKeys = data.data.keys; // ordered array of "MM-YYYY"
        const pastTargetsEntries = data.data.parameters; // object with dates as keys
        const pastTargetsOrderedList = pastTargetsKeys.map((date) => {
          return {
            "Input Date": date,
            ...pastTargetsEntries[date]
          }; // List of Parameter Objects with date
        }).reverse(); // newest to oldest

        console.log("Processed past targets:", pastTargetsOrderedList);

        // Set employee details from user
        setEmployeeDetails(user);

        // Set past targets from API
        setPastTargets(pastTargetsOrderedList);

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

    loadParameters();

    // Cleanup function to abort fetch if component unmounts
    return () => ac.abort();

  }, [user])

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

  // Handle file upload
  const handleFileUpload = async (file) => {
    // const formData = new FormData();
    // formData.append('file', file);
    // formData.append('employee_id', user.id);

    // const response = await fetch('http://localhost:5000/parameter/upload', {
    //   method: 'POST',
    //   body: formData,
    // });

    // if (!response.ok) {
    //   throw new Error(`HTTP Error! Status: ${response.status}`);
    // }

    // const result = await response.json();
    // console.log('Upload success:', result);

    // // Refresh the parameters list
    // // You might want to refetch the data here or add the new data to pastTargets
    // window.location.reload(); // Simple approach, or call your loadParameters function
  };


  // Handle Update button (Update DB with new Targets) 
  const handleUpdate = async () => {
    if (!newTargets) return;
    setSaving(true);

    try {
      const response = await fetch(`http://localhost:5000/parameter/batch/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "employee_id": user.id,
          "parameters": newTargets
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP Error! Status: ${response.status}`);
      }

      const result = await response.json();
      console.log("Success:", result);

      // Add the new row to past targets for immediate UI update
      const newRow = {
        "Input Date": getCurrentDateFormatted(),
        ...newTargets
      };
      setPastTargets(prev => [newRow, ...prev]);

      // Clear the form or reset to defaults
      setNewTargets(null);

    } catch (err) {
      console.error("Error saving targets:", err);
      setError(err.message);
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

        {user.role === "Accountant" && (
          <button
            className="mr-10 rounded-xl bg-gray-600 px-6 py-3 text-xl font-extrabold text-white cursor-pointer hover:bg-gray-700 transition"
            onClick={() => setIsUploadModalOpen(true)}
          >
            Upload File
          </button>
        )}


        <button
          className="rounded-xl bg-indigo-700 px-6 py-3 text-xl font-extrabold text-white cursor-pointer"
          onClick={handleUpdate}
          disabled={saving || !newTargets}
        >
          {saving ? "Updating..." : "Update"}
        </button>
      </div>

      {/* File Upload Modal */}
      {
        user.role === "Accountant" && (
          <FileUploadModal
            isOpen={isUploadModalOpen}
            onClose={() => setIsUploadModalOpen(false)}
            onSubmit={handleFileUpload}
          />
        )
      }
    </main>
  );
}