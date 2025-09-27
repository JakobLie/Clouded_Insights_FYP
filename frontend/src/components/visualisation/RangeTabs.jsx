"use client";
import { useState } from "react";

export default function RangeTabs({ currentRange, onChange }) {
  const [active, setActive] = useState(currentRange);
  const click = (monthRange) => {
    setActive(monthRange);
    onChange && onChange(monthRange);
  };

  const baseClass = "px-3 py-1 rounded-md border text-sm transition shadow-sm";
  const mutedClass = "bg-gray-100 border-gray-300 hover:bg-gray-50 cursor-pointer";
  const activeClass = "bg-gray-500 text-white border-gray-700";

  return (
    <div className="inline-flex gap-2">
      {["3M", "6M", "12M"].map((monthRange) => (
        <button
          key={monthRange}
          className={`${baseClass} ${active === monthRange ? activeClass : mutedClass}`}
          onClick={() => click(monthRange)}
        >
          {monthRange}
        </button>
      ))}
    </div>
  );
}
