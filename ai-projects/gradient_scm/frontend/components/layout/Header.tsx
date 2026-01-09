// frontend/components/layout/Header.tsx
"use client";

export default function Header() {
  return (
    <header className="h-14 border-b bg-white flex items-center px-4 justify-between">
      <h1 className="text-sm font-semibold text-slate-700">
        Admin Console
      </h1>

      <div className="text-xs text-slate-500">
        Logged in (session)
      </div>
    </header>
  );
}
