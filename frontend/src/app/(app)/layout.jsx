import Navbar from "@/components/Navbar";
import Breadcrumbs from "@/components/Breadcrumbs";

export default function AppLayout({ children }) {
  return (
    <>
      <Navbar />
      <section className=" bg-gray-50">
        <div className="mx-auto max-w-6xl p-4 sm:p-6 space-y-4">
          <Breadcrumbs />
        </div>
      </section>
      {children}
    </>
  );
}