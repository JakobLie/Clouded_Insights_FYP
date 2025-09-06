"use client";
import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-6 py-3 bg-white shadow border-b border-gray-200">
      <h1 className="font-bold text-lg text-gray-800">TSH ERP Dashboard</h1>
      <div className="space-x-4">
        <Link href="/upload" className="text-gray-700 hover:text-blue-600">
          Upload CSV
        </Link>
        <Link href="/notifications" className="text-gray-700 hover:text-blue-600">
          🔔 Notifications
        </Link>
        <Link href="/" className="text-gray-700 hover:text-blue-600">
          Log Out
        </Link>
      </div>
    </nav>
  );
}
