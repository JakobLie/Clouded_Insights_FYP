import Image from "next/image";

export default function Login() {
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

            <form className="mt-6 space-y-4">
              {/* Email */}
              <div className="space-y-1">
                <label htmlFor="email" className="text-sm font-medium text-gray-700">
                  Email
                </label>
                <input
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
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  className="w-full rounded-md border border-gray-300 bg-white px-3 py-2 outline-none focus:border-gray-500"
                />
              </div>

              {/* Submit */}
              <div className="pt-2">
                <button
                  type="button" /* wire up later */
                  className="w-full rounded-md bg-gray-600 px-4 py-2 text-white font-semibold tracking-wide hover:bg-gray-700"
                >
                  SUBMIT
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>
    </main>
  );
}
