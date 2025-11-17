"use client";

const ACCENT_MAP = {
  gray: "bg-gray-200 border-gray-300",
  red: "bg-red-200 border-red-300",
  yellow: "bg-yellow-200 border-yellow-300",
  green: "bg-green-200 border-green-300"
};

export default function StatCard({ title, lines, accent, active, onClick }) {

  return (
    <button
      type="button"
      onClick={onClick}
      className={`w-full text-left rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 ${active ? "ring-2 ring-sky-500 cursor-default" : "hover:ring-2 hover:ring-gray-300 cursor-pointer"
        }`}
    >
      <div className={`rounded-xl border p-4 ${ACCENT_MAP[accent]} shadow-sm`}>
        <div className="font-semibold mb-2">{title}</div>
        <div className="space-y-1 text-sm">
          {lines?.map((l, i) => (
            <div key={i}>
              <span className="font-semibold">{l.label}: </span>
              <span>{l.value}</span>
            </div>
          ))}
        </div>
      </div>
    </button>
  );
}
