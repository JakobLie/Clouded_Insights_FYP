"use client"

import Link from "next/link";
import Image from "next/image";
import { useState, useEffect } from "react";

const API_BASE_URL = "http://localhost:5000";

export default function Navbar({userDetails}) {

  const employee = {
    id: userDetails.id,
    name: userDetails.name,
    email: userDetails.email,
    role: userDetails.role,
    business_unit: userDetails.business_unit,
  }

  const [unreadCount, setUnreadCount] = useState(0);

  // Fetch unread notification count
  useEffect(() => {
    if (!employee.id) return;

    const fetchUnreadCount = async () => {
      try {
        const response = await fetch(
          `${API_BASE_URL}/notifications/${employee.id}`
        );
        const data = await response.json();

        if (response.ok && data.code === 200) {
          const unread = data.data.filter(n => !n.is_read).length;
          setUnreadCount(unread);
        }
      } catch (err) {
        console.error("Error fetching notification count:", err);
      }
    };

    fetchUnreadCount();

    // Poll for new notifications every 30 seconds
    const interval = setInterval(fetchUnreadCount, 30000);

    return () => clearInterval(interval);
  }, [employee.id]);

  return (
    <nav className="flex items-center justify-between bg-[#3A5C8B] px-6 py-3 text-white">
      {/* Left section */}
      <div className="flex items-center gap-3">

        {/* Profile Image Placeholder */}
        <div style={{
          borderRadius: '50%',
          overflow: 'hidden'
        }}>
          <Image
            src={"/profile-pic.jpg"}
            height={75}
            width={75}
            alt="profile picture"
          />
        </div>

        {/* Username and Business Unit */}
        <span className="text-2xl font-medium">{employee.name} [{employee.business_unit}]</span>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-6 text-xl font-medium">
        <Link href="/profit">Home</Link>
        <Link href="/setup">Set Up</Link>
        <Link href="/notifications" className="relative">
          Notifications
          {unreadCount > 0 && (
            <span className="absolute -top-2 -right-3 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-xs font-bold text-white">
              {unreadCount > 9 ? '9+' : unreadCount}
            </span>
          )}
        </Link>
        <Link href="/login">Log Out</Link>
      </div>
    </nav>
  );
}