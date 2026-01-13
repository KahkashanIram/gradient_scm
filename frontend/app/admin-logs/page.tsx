
"use client";

import { useEffect, useState, useRef } from "react";
import { apiFetch } from "@/lib/api";
import AdminActivityLogTable from "@/components/admin/AdminActivityLogTable";
import {
  AdminActivityLog,
  AdminActivityLogResponse,
} from "@/types/admin";

const AUTO_REFRESH_INTERVAL = 10_000; // 10 seconds

export default function AdminLogsPage() {
  const [logs, setLogs] = useState<AdminActivityLog[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Prevent overlapping fetches
  const isFetching = useRef(false);

  const fetchLogs = async () => {
    if (isFetching.current) return;
    isFetching.current = true;

    try {
      const res = await apiFetch<AdminActivityLogResponse>(
        "/api/admin/activity-logs/"
      );
      setLogs(res.results);
      setError(null);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to load admin activity logs");
      }
    } finally {
      setLoading(false);
      isFetching.current = false;
    }
  };

  // Initial load
  useEffect(() => {
    fetchLogs();
  }, []);

  // Auto refresh
  useEffect(() => {
    const interval = setInterval(fetchLogs, AUTO_REFRESH_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="p-4 text-sm text-gray-500">
        Loading admin activity logs…
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-sm text-red-600">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold">
          Admin Activity Logs
        </h1>

        <span className="text-xs text-gray-500">
          Auto-refresh every 10s
        </span>
      </div>

      <AdminActivityLogTable logs={logs} />
    </div>
  );
}
