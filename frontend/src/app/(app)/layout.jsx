import { SetupProvider } from "./providers/SetupProvider";

import Navbar from "../../components/Navbar";

export default function AppLayout({ children }) {
  return (
    <SetupProvider>
      <div className="flex h-screen bg-gray-100">

        {/* Main content area */}
        <div className="flex flex-col flex-1">
          {/* Navbar */}
          <Navbar />

          {/* Page content */}
          <main className="flex-1 p-6 overflow-y-auto">
            {children}
          </main>
        </div>
      </div>
    </SetupProvider>
  );
}
