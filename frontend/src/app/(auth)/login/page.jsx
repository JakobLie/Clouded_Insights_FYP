"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import Image from "next/image";

export default function Login() {
  const router = useRouter();
  const { setUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [popupOpen, setPopupOpen] = useState(false);
  const [popupMsg, setPopupMsg] = useState("");
  const [error, setError] = useState(null);

  async function onSubmit(event) {
    event.preventDefault();
    setError(null);
    setLoading(true);

    const form = new FormData(event.currentTarget);
    const body = {
      email: String(form.get("email") || ""),
      password: String(form.get("password") || "")
    };

    try {
      const result = await fetch("http://localhost:5000/employee/authenticate/",
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(body)
        }
      );

      // Parse JSON once
      const json = await result.json();

      if (!result.ok) {
        // Show error popup
        setPopupMsg(json?.message || `Login failed (status ${result.status})`);
        setPopupOpen(true);
        setError(json?.message || "Login failed");
        return; // Don't proceed further
      }

      const user = json?.data;
      if (!user) {
        setPopupMsg("Login succeeded but no user data returned.");
        setPopupOpen(true);
        setError("No user data returned");
        return;
      }

      // Success - show success message
      setPopupMsg(json?.message || "Login successful!");
      setPopupOpen(true);
      setUser(user);

      // Close popup then redirect with small delay so user sees message
      setTimeout(() => {
        setPopupOpen(false);
        router.push("/setup");
      }, 1000);

    } catch (error) {
      setError(error.message || "Login failed");
      setPopupMsg(error.message || "An error occurred during login");
      setPopupOpen(true);
    } finally {
      setLoading(false);
    }

  }


  return (
    <main className="min-h-screen bg-gray-50">
      {/* Top banner GIF */}
      {/* Put your GIF in /public/hero.gif (see note below) */}
      <div className="border-b">
        {/* Use <img> to keep GIF animation reliable */}
        <img
          src="/manufacturing-factory-cropped.gif"
          alt="Factory animation"
          className="
            w-full
            h-[140px] sm:h-[200px] md:h-[280px] lg:h-[380px] xl:h-[480px]
            object-cover object-bottom
          "
        />
      </div>

      {/* Content */}
      <section className="mx-auto max-w-6xl px-4 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left: Welcome + Logo */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <p className="text-lg text-gray-700">Welcome to the</p>
            <h1 className="mt-2 text-3xl font-semibold">
              <span className="tracking-wide">Traffic-light </span>
              <span className="font-bold">Simulation Hub</span>
            </h1>

            <div className="mt-8">
              {/* Replace with your real logo file in /public */}
              <Image
                src={"/tsh-logo.png"}
                alt="TSH Group"
                width={150}
                height={150}
                unoptimized
                className="h-20 w-auto"
              />
              <p className="mt-3 text-sm text-gray-500">
                <br /><br />
                © TSH Group — Internal Simulation Portal
              </p>
            </div>
          </div>

          {/* Right: Login card */}
          <div className="bg-gray-100 rounded-lg border border-gray-200 p-6">
            <h2 className="text-2xl font-bold tracking-wide text-center">LOGIN</h2>

            <form className="mt-6 space-y-4" onSubmit={onSubmit}>
              {/* Email */}
              <div className="space-y-1">
                <label htmlFor="email" className="text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
                  name="email"
                  id="email"
                  type="email"
                  placeholder="user@company.com"
                  className="w-full rounded-md border border-gray-300 bg-white px-3 py-2 outline-none focus:border-gray-500"
                />
              </div>

              {/* Password */}
              <div className="space-y-1">
                <label htmlFor="password" className="text-sm font-medium text-gray-700">
                  Password
                </label>
                <input
                  name="password"
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  className="w-full rounded-md border border-gray-300 bg-white px-3 py-2 outline-none focus:border-gray-500"
                />
              </div>

              {error && <p className="text-sm text-red-600">{error}</p>}
              {/* Submit */}
              <div className="pt-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full rounded-md bg-gray-600 px-4 py-2 text-white font-semibold tracking-wide hover:bg-gray-700"
                >
                  {loading ? "Signing in…" : "SUBMIT"}
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      {/* Simple Popup Modal */}
      {popupOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-white rounded-lg shadow-lg max-w-sm w-full p-5">
            <h3 className="text-lg font-semibold mb-2">Login Status</h3>
            <p className="text-gray-700">{popupMsg}</p>
            <div className="mt-4 flex justify-end gap-2">
              <button
                onClick={() => setPopupOpen(false)}
                className="rounded-md border px-4 py-2"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
