"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import HealthCard from "@/components/health/HealthCard";
import { SystemHealthResponse } from "@/types/system";

export default function SystemHealthPage() {
  const [data, setData] = useState<SystemHealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const fetchHealth = async () => {
    try {
      const res = await apiFetch<SystemHealthResponse>(
        "/api/system/health/"
      );
      setData(res);
      setLastUpdated(new Date());
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Failed to fetch system health");
      }
    }
  };

  useEffect(() => {
    let isMounted = true;
    let timeoutId: ReturnType<typeof setTimeout>;

    const poll = async () => {
      if (!isMounted) return;

      await fetchHealth();

      // Schedule next refresh AFTER request completes
      timeoutId = setTimeout(poll, 30_000);
    };

    poll(); // initial fetch + loop

    return () => {
      isMounted = false;
      clearTimeout(timeoutId);
    };
  }, []);

  if (error) {
    return <div className="text-red-600">{error}</div>;
  }

  if (!data) {
    return <div>Loading system health…</div>;
  }

  const { application, database, system } = data.components;

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold">System Health</h1>

        {lastUpdated && (
          <span className="text-xs text-slate-500">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </span>
        )}
      </div>

      {/* Health Cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {/* Application */}
        <HealthCard title="Application" status={application.status}>
          <div>Service: {application.details.service}</div>
        </HealthCard>

        {/* Database */}
        <HealthCard title="Database" status={database.status}>
          <div>Engine: {database.details.engine}</div>
        </HealthCard>

        {/* System */}
        {/* System */}
<HealthCard title="System" status={system.status}>
  <div className="space-y-1">
    {/* CPU */}
    <div>
      <span className="font-medium">CPU:</span>{" "}
      {system.details.cpu_percent}%
    </div>

    {/* Memory */}
    <div>
      <span className="font-medium">Memory:</span>{" "}
      {system.details.memory_percent}% (
      {system.details.memory_available_mb.toFixed(0)} MB free /{" "}
      {system.details.memory_total_mb.toFixed(0)} MB)
    </div>

    {/* Disk */}
    <div>
      <span className="font-medium">Disk:</span>{" "}
      {system.details.disk_percent}% (
      {system.details.disk_free_gb.toFixed(1)} GB free /{" "}
      {system.details.disk_total_gb.toFixed(1)} GB)
    </div>
  </div>
</HealthCard>

      </div>
    </div>
  );
}
