"use client"

import NotificationItem from "@/app/(app)/notifications/NotificationItem";
import { useState, useEffect } from "react";
import { useAuth } from "@/components/AuthProvider";
import { useRouter } from "next/navigation";

const API_BASE_URL = "http://localhost:5000";

export default function Notifications() {
  // Get User Object
  const { user, logout } = useAuth();
  const router = useRouter();

  // Set React Hooks
  const [notifications, setNotifications] = useState([]);

  // UX state
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Redirect if not logged in
  useEffect(() => {
    if (!user) {
      router.replace("/login");
    }
  }, [user, router]);

  // Fetch all notifications for the logged-in user
  useEffect(() => {
    if (!user || !user.id) return;

    const ac = new AbortController();

    async function loadNotificationData() {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(
          `${API_BASE_URL}/notifications/${user.id}`,
          { signal: ac.signal }
        );

        const data = await response.json();

        if (response.ok && data.code === 200) {
          setNotifications(data.data);
        } else {
          setError(data.message || "Failed to load notifications");
          setNotifications([]);
        }
      } catch (err) {
        if (err.name !== "AbortError") {
          setError("Error loading notifications");
          console.error(err);
        }
      } finally {
        setLoading(false);
      }
    }

    loadNotificationData();

    return () => ac.abort();
  }, [user]);

  // Delete a notification
  const handleDelete = async (notificationId) => {
    try {
      console.log('Deleting notification:', notificationId);
      const response = await fetch(
        `${API_BASE_URL}/notifications/${notificationId}`,
        { method: "DELETE" }
      );

      console.log('Delete response status:', response.status);
      const data = await response.json();
      console.log('Delete response data:', data);

      if (response.ok && data.code === 200) {
        // Remove from state
        setNotifications((prev) =>
          prev.filter((n) => n.id !== notificationId)
        );
        console.log('Notification deleted successfully');
      } else {
        console.error('Delete failed:', data);
        alert(data.message || "Failed to delete notification");
      }
    } catch (err) {
      console.error("Error deleting notification:", err);
      alert("Error deleting notification: " + err.message);
    }
  };

  // Mark a notification as read
  const handleMarkAsRead = async (notificationId) => {
    try {
      console.log('Marking notification as read:', notificationId);
      const response = await fetch(
        `${API_BASE_URL}/notifications/${notificationId}/read`,
        { method: "PATCH" }
      );

      console.log('Mark as read response status:', response.status);
      const data = await response.json();
      console.log('Mark as read response data:', data);

      if (response.ok && data.code === 200) {
        // Update state
        setNotifications((prev) =>
          prev.map((n) =>
            n.id === notificationId
              ? { ...n, is_read: true }
              : n
          )
        );
        console.log('Notification marked as read successfully');
      } else {
        console.error('Mark as read failed:', data);
      }
    } catch (err) {
      console.error("Error marking notification as read:", err);
    }
  };

  // Mark all notifications as read
  const handleMarkAllAsRead = async () => {
    if (!user || !user.id) return;

    try {
      console.log('Marking all notifications as read for employee:', user.id);
      const response = await fetch(
        `${API_BASE_URL}/notifications/${user.id}/read_all`,
        { method: "PATCH" }
      );

      console.log('Mark all as read response status:', response.status);
      const data = await response.json();
      console.log('Mark all as read response data:', data);

      if (response.ok && data.code === 200) {
        // Update all notifications in state
        setNotifications((prev) =>
          prev.map((n) => ({ ...n, is_read: true }))
        );
        console.log('All notifications marked as read successfully');
      } else {
        console.error('Mark all as read failed:', data);
        alert(data.message || "Failed to mark all as read");
      }
    } catch (err) {
      console.error("Error marking all as read:", err);
      alert("Error marking all as read: " + err.message);
    }
  };

  // Format timestamp - already formatted by backend
  const formatTimestamp = (timestamp) => {
    // Backend returns format: '%d-%m-%Y %H:%M:%S'
    // Convert to a more readable format
    if (!timestamp) return "";
    
    try {
      const [datePart, timePart] = timestamp.split(' ');
      const [day, month, year] = datePart.split('-');
      const [hour, minute] = timePart.split(':');
      
      const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      
      const hourNum = parseInt(hour);
      const period = hourNum >= 12 ? "PM" : "AM";
      const hour12 = hourNum % 12 || 12;
      
      return `${day} ${monthNames[parseInt(month) - 1]} ${year} at ${hour12}:${minute} ${period}`;
    } catch (e) {
      return timestamp; // Return as-is if parsing fails
    }
  };

  // Map notification data to component props
  const mapNotificationToProps = (notification) => {
    // Parse the body as JSON to extract structured data
    let lines = [];
    try {
      const bodyData = JSON.parse(notification.body);
      lines = Object.entries(bodyData).map(([label, value]) => ({
        label: label.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase()),
        value: String(value),
      }));
    } catch (e) {
      // If body is not JSON, treat it as plain text
      lines = [{ label: "Message", value: notification.body }];
    }

    return {
      id: notification.id,
      variant: notification.type.toLowerCase() === "alert" ? "alert" : "warning",
      title: notification.subject,
      timestamp: formatTimestamp(notification.created_at),
      isRead: notification.is_read,
      lines: lines,
    };
  };

  if (loading) {
    return (
      <main className="mx-auto max-w-4xl p-4 sm:p-6">
        <div className="text-center text-gray-600">Loading notifications...</div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="mx-auto max-w-4xl p-4 sm:p-6">
        <div className="text-center text-red-600">{error}</div>
      </main>
    );
  }

  const hasUnreadNotifications = notifications.some((n) => !n.is_read);

  // Sort notifications: unread first (by recency), then read (by recency)
  const sortedNotifications = [...notifications].sort((a, b) => {
    // If read status differs, unread comes first
    if (a.is_read !== b.is_read) {
      return a.is_read ? 1 : -1;
    }
    
    // If same read status, sort by timestamp (most recent first)
    // Parse timestamps for comparison
    try {
      const parseTimestamp = (ts) => {
        const [datePart, timePart] = ts.split(' ');
        const [day, month, year] = datePart.split('-');
        const [hour, minute, second] = timePart.split(':');
        return new Date(year, month - 1, day, hour, minute, second);
      };
      
      const dateA = parseTimestamp(a.created_at);
      const dateB = parseTimestamp(b.created_at);
      
      return dateB - dateA; // Most recent first
    } catch (e) {
      return 0; // Keep original order if parsing fails
    }
  });

  return (
    <main className="mx-auto max-w-4xl p-4 sm:p-6 bg-gray-50">
      <div className="flex items-center justify-between mb-4">
        {hasUnreadNotifications && (
          <button
            onClick={handleMarkAllAsRead}
            className="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors"
          >
            Mark all as read
          </button>
        )}
      </div>

      {notifications.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          No notifications found
        </div>
      ) : (
        <div className="space-y-3">
          {sortedNotifications.map((n) => (
            <NotificationItem
              key={n.id}
              {...mapNotificationToProps(n)}
              onDelete={handleDelete}
              onMarkAsRead={handleMarkAsRead}
            />
          ))}
        </div>
      )}
    </main>
  );
}

