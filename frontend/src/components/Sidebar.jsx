"use client";
import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-800 text-white flex flex-col">
      <div className="px-6 py-4 font-bold text-xl border-b border-gray-700">
        ERP App
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2">
        <Link
          href="/dashboard"
          className="block px-3 py-2 rounded hover:bg-gray-700"
        >
          Dashboard
        </Link>
        <Link
          href="/notifications"
          className="block px-3 py-2 rounded hover:bg-gray-700"
        >
          Notifications
        </Link>
        <Link
          href="/reports"
          className="block px-3 py-2 rounded hover:bg-gray-700"
        >
          Reports
        </Link>
      </nav>
    </aside>
  );
}
