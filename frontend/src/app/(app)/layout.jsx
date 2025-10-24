"use client"

import Navbar from "@/components/Navbar";
import Breadcrumbs from "@/components/Breadcrumbs";
import { useAuth } from "@/components/AuthProvider";

export default function AppLayout({ children }) {

  const { user } = useAuth();

  return (
    <>
      <Navbar userDetails={user} /> 
      <section className=" bg-gray-50">
        <div className="mx-auto max-w-6xl p-4 sm:p-6 space-y-4">
          <Breadcrumbs />
        </div>
      </section>
      {children}
    </>
  );
}