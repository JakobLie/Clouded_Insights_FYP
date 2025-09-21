import { getCurrentDateFormatted } from "@/utils/time-utils";

export default function KPITable({ defaultKPIValues, parameters }) {

  const KPINames = Object.keys(defaultKPIValues || {});
  const previousTargetsByDate = parameters.entries;
  const previousTargetsOrderedDates = parameters.keys.reverse(); // Use reverse() to order Newest to Oldest

  return (
    <section className="rounded-xl">
      {/* Scroll container */}
      <div className="overflow-x-auto rounded-xl">
        <table className="min-w-max w-full text-sm ">
          {/* Sticky header */}
          <thead className="bg-slate-600 text-white sticky top-0 ">
            <tr className="[&>th]:px-4 [&>th]:py-3 [&>th]:font-semibold ">
              <th className="text-center whitespace-nowrap">Sales target (SGD)</th>
              <th className="text-center whitespace-nowrap">Cost budget (SGD)</th>

              {KPINames.map((KPIName) => (
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
                  className="h-10 rounded-md bg-gray-200 px-3 py-2 text-center"
                />
              </td>
              <td>
                <input
                  type="number"
                  className="h-10 rounded-md bg-gray-200 px-3 py-2 text-center"
                />
              </td>

              {KPINames.map((KPIName) => (
                <td key={KPIName}>
                  <input
                    type="number"
                    className="h-10 rounded-md bg-gray-200 px-3 py-2 text-center"
                    placeholder={(defaultKPIValues[KPIName] * 100).toFixed(0)}
                  />
                </td>
              ))}

              <td className="whitespace-nowrap">{getCurrentDateFormatted()}</td>
            </tr>

            {/* Historical rows */}
            {(previousTargetsOrderedDates || {}).map((date) => (
              <tr key={previousTargetsByDate[date]["Input Date"]} className="border-t">
                <td className="whitespace-nowrap">
                  {previousTargetsByDate[date]["Sales Target"] ?? "—"}
                </td>
                <td className="whitespace-nowrap">
                  {previousTargetsByDate[date]["Cost Budget"] ?? "—"}
                </td>

                {KPINames.map((KPIName) => (
                  <td key={`${previousTargetsByDate[date]["Input Date"]}-${KPIName}`} className="whitespace-nowrap">
                    {previousTargetsByDate[date][KPIName] !== undefined ? `${(previousTargetsByDate[date][KPIName] * 100).toFixed(0)}` : "—"}
                  </td>
                ))}

                <td className="whitespace-nowrap">{previousTargetsByDate[date]["Input Date"]}</td>
              </tr>
            ))}

          </tbody>
        </table>
      </div>
    </section>
  );
}