"use client"

import Link from "next/link";
import Image from "next/image";

export default function Navbar() {

  const employee = {
    id: "12345",
    name: "Lie Wie Yong Jakob",
    email: "jakob.lie.2022@scis.smu.edu.sg",
    role: "BU Manager",
    business_unit: "BB1",
    password_hash: "hashedString",
    created_at: "17-09-2025"
  }

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
        <Link href="/notifications">Notifications</Link>
        <Link href="/login">Log Out</Link>
      </div>
    </nav>
  );
}
