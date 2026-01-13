// frontend/components/layout/Sidebar.tsx
"use client";

import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white shrink-0 hidden md:flex">
      <div className="w-full p-4">
        {/* App Title */}
        <h2 className="text-lg font-semibold mb-6">
          GRADIENT SCM
        </h2>

        {/* Navigation */}
        <nav className="space-y-2 text-sm">
          {/* Dashboard */}
          <Link
            href="/"
            className="block hover:text-slate-300"
          >
            Dashboard
          </Link>

          {/* System */}
          <Link
            href="/system"
            className="block hover:text-slate-300"
          >
            System Health
          </Link>

          {/* Inventory placeholder */}
          <span className="block text-slate-400 mt-4">
            Inventory (coming)
          </span>

          {/* ===== Audit Section ===== */}
          <div className="mt-6">
            <div className="text-xs uppercase text-slate-400 mb-2">
              Audit
            </div>

            <Link
              href="/admin-logs"
              className="block hover:text-slate-300"
            >
              Activity Logs
            </Link>
          </div>
        </nav>
      </div>
    </aside>
  );
}
