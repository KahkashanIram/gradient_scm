"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import AdminActivityLogTable from "@/components/admin/AdminActivityLogTable";
import {
  AdminActivityLog,
  AdminActivityLogResponse,
} from "@/types/admin";

export default function AdminLogsPage() {
  const [logs, setLogs] = useState<AdminActivityLog[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    try {
      const res = await apiFetch<AdminActivityLogResponse>(
        "/api/admin/activity-logs/"
      );
      setLogs(res.results);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to load admin activity logs");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  if (loading) {
    return <div>Loading admin activity logs…</div>;
  }

  if (error) {
    return <div className="text-red-600">{error}</div>;
  }

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">
        Admin Activity Logs
      </h1>

      <AdminActivityLogTable logs={logs} />
    </div>
  );
}
