"use client";

function ClockIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.8" {...props}>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3 2" />
    </svg>
  );
}

function TrashIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="1.8" {...props}>
      <path d="M3 6h18" />
      <path d="M8 6v-2a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
      <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
      <path d="M10 11v6M14 11v6" />
    </svg>
  );
}

export default function NotificationItem({
  variant = "warning", // "alert" | "warning"
  title,
  lines = [],          // [{ label: string, value: string }]
  timestamp = "12 Sep 2025 at 7:12 PM",
}) {
  const badge = {
    alert:  { text: "ALERT",   cls: "bg-red-600 text-white" },
    warning:{ text: "WARNING", cls: "bg-amber-400 text-white" },
  }[variant] || { text: "INFO", cls: "bg-gray-300 text-gray-800" };

  return (
    <article className="rounded-md border border-gray-300 bg-white">
      {/* header row: badge + title + timestamp */}
      <div className="flex items-start justify-between gap-3 p-3">
        <div className="flex items-center gap-3">
          <span className={`text-xs font-bold px-2 py-1 rounded ${badge.cls}`}>
            {badge.text}
          </span>
          <h3 className="font-semibold text-gray-900">
            {title}
          </h3>
        </div>

        <div className="flex items-center gap-2 text-gray-500 text-sm">
          <ClockIcon />
          <span className="whitespace-nowrap">{timestamp}</span>
        </div>
      </div>

      {/* body: lines */}
      <div className="px-3 pb-3 text-sm text-gray-600">
        <div className="space-y-1">
          {lines.map((l, i) => (
            <p key={i}>
              <span className="font-medium">{l.label}: </span>
              <span>{l.value}</span>
            </p>
          ))}
        </div>
      </div>

      {/* footer: actions (trash) */}
      <div className="flex justify-end px-3 pb-3">
        <button
          type="button"
          className="inline-flex items-center rounded p-1.5 text-gray-500 hover:text-gray-700 hover:bg-gray-100"
          aria-label="Delete notification"
          // onClick={() => ...}
        >
          <TrashIcon />
        </button>
      </div>
    </article>
  );
}
