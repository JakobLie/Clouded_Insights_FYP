import Image from "next/image";
import KPITable from "./KPITable";
import parametersData from "../../../mock_data/setupPage/GetAllParametersByEmployeeId.json";
import employeeData from "../../../mock_data/setupPage/GetEmployeeByEmployeeId.json";

export default function Setup() {

  const defaultKPIValues = {
    "Gross Profit Margin": 0.53,
    "Operating Profit Margin": 0.42,
    "Net Profit Margin": 0.31,
    "Quick Ratio": 0.33,
    "Return On Sales": 0.24,
    "Days Sales Outstanding": 0.42,
    "Receivables Turnover": 0.55,
    "Cost Of Goods Sold Ratio": 0.66,
    "Days Payable Outstanding": 0.47,
    "Overhead Ratio": 0.39
  }

  const employee = employeeData.data;
  const parameters = parametersData.data;

  return (
    <main className="mx-auto max-w-5xl p-6 space-y-6">
      {/* Header card */}
      <section className="rounded-2xl bg-gray-200 p-6 shadow-sm">
        <div className="flex items-center justify-between border-b border-gray-300 pb-3">
          <div className="text-sm font-semibold text-white">
            <span className="rounded-lg bg-slate-600 px-3 py-1">Employee ID: {employee.id}</span>
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
              <h1 className="text-3xl font-extrabold leading-tight">{employee.name}</h1>
            </div>
          </div>

          {/* Job info */}
          <div className="md:text-right">
            <div className="text-xl font-bold">Job Title:</div>
            <div className="text-xl">{employee.role}</div>
            <div className="mt-2 text-xl font-bold">Business Unit(s):</div>
            <div className="text-xl">{employee.business_unit}</div>
          </div>
        </div>
      </section>

      {/* Columns header (tabs look) */}
      <KPITable defaultKPIValues={defaultKPIValues} parameters={parameters} />

      {/* Footer actions */}
      <div className="flex justify-end">
        <button className="rounded-xl bg-indigo-700 px-6 py-3 text-xl font-extrabold text-white">
          Update
        </button>
      </div>
    </main>
  );
}