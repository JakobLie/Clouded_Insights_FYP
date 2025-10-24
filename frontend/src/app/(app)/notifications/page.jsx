import NotificationItem from "@/app/(app)/notifications/NotificationItem";
import { useState, useEffect } from "react";
import { useAuth } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";



const SAMPLE = [
  {
    variant: "alert",
    title: "Prediction for January Profit is more than 5% below Target",
    timestamp: "12 Sep 2025 at 7:12 PM",
    lines: [
      { label: "Predicted Profit", value: "SGD1,000,000" },
      { label: "Target Profit", value: "SGD2,000,000" },
    ],
  },
  {
    variant: "warning",
    title: "Prediction for Sales is <5% below Target",
    timestamp: "11 Sep 2025 at 2:12 PM",
    lines: [
      { label: "Predicted Sales", value: "SGD1,910,000" },
      { label: "Target Sales", value: "SGD2,000,000" },
    ],
  },
  {
    variant: "warning",
    title: "Prediction for Cost is <5% over Budget",
    timestamp: "09 Sep 2025 at 2:12 PM",
    lines: [
      { label: "Predicted Cost", value: "SGD1,000,000" },
      { label: "Target Budget", value: "SGD1,030,000" },
    ],
  },
];

export default function Notifications() {

  // Get User Object
  const { user, logout } = useAuth();
  const router = useRouter();

  // Set React Hooks
  const [notifications, setNotifications] = useState({})

  // UX state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Redirect if not logged in
  useEffect(() => {
    if (!user) {
      router.replace("/login");
    };
  }, [user, router]);

  // // Fetch all data once we have a user
  // useEffect(() => {
  //   if (!user) return;

  //   const ac = new AbortController();

  //   async function loadNotificationData() {
  //     setLoading(true);
  //     setError(null);
  //   }

  //   try {
  //     const notifications = await fetch(`http://localhost:5000/`)
  //   } catch (error) {
      
  //   }
  // })

  return (
    <main className="mx-auto max-w-4xl p-4 sm:p-6">
      <h1 className="sr-only">Notifications</h1>

      <div className="space-y-3">
        {SAMPLE.map((n, i) => (
          <NotificationItem
            key={i}
            variant={n.variant}
            title={n.title}
            lines={n.lines}
            timestamp={n.timestamp}
          />
        ))}
      </div>
    </main>
  );
}
