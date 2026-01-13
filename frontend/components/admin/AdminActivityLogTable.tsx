"use client";

import { AdminActivityLog } from "@/types/admin";

type Props = {
  logs: AdminActivityLog[];
};

export default function AdminActivityLogTable({ logs }: Props) {
  return (
    <div className="overflow-x-auto rounded-lg border bg-white">
      <table className="min-w-full border-collapse text-sm">
        <thead className="bg-slate-100 text-slate-600">
          <tr>
            <th className="px-3 py-2 text-left font-medium">Time</th>
            <th className="px-3 py-2 text-left font-medium">Admin</th>
            <th className="px-3 py-2 text-left font-medium">Action</th>
            <th className="px-3 py-2 text-left font-medium">Module</th>
            <th className="px-3 py-2 text-left font-medium">Object</th>
            <th className="px-3 py-2 text-left font-medium">Metadata</th>
          </tr>
        </thead>

        <tbody className="divide-y">
          {logs.length === 0 && (
            <tr>
              <td
                colSpan={6}
                className="px-3 py-6 text-center text-slate-500"
              >
                No activity logs found
              </td>
            </tr>
          )}

          {logs.map((log) => (
            <tr key={log.id} className="hover:bg-slate-50">
              <td className="px-3 py-2 whitespace-nowrap">
                {new Date(log.created_at).toLocaleString()}
              </td>

              <td className="px-3 py-2">
                {log.admin_user}
              </td>

              <td className="px-3 py-2">
                <span className="rounded bg-slate-100 px-2 py-0.5 text-xs">
                  {log.action}
                </span>
              </td>

              <td className="px-3 py-2">
                {log.module}
              </td>

              <td className="px-3 py-2">
                {log.object_id ?? "-"}
              </td>

              <td className="px-3 py-2 max-w-xs truncate text-slate-600">
                {Object.keys(log.metadata || {}).length > 0
                  ? JSON.stringify(log.metadata)
                  : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
