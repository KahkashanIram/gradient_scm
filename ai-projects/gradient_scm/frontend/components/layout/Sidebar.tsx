// frontend/components/layout/Sidebar.tsx
"use client";

import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white shrink-0 hidden md:flex">
      <div className="w-full p-4">
        <h2 className="text-lg font-semibold mb-6">GRADIENT SCM</h2>

        <nav className="space-y-2 text-sm">
          <Link href="/" className="block hover:text-slate-300">
            Dashboard
          </Link>

          <Link href="/system" className="block hover:text-slate-300">
            System Health
          </Link>

          <span className="block text-slate-400 mt-4">
            Inventory (coming)
          </span>

          <span className="block text-slate-400">
            Admin Logs (coming)
          </span>
        </nav>
      </div>
    </aside>
  );
}
