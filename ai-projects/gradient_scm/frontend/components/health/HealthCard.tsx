// frontend/components/health/HealthCard.tsx
import clsx from "clsx";

type Props = {
  title: string;
  status: string;
  children?: React.ReactNode;
};

const statusColor = (status: string) => {
  switch (status) {
    case "ok":
      return "bg-emerald-50 text-emerald-700 border-emerald-200";
    case "warning":
      return "bg-amber-50 text-amber-700 border-amber-200";
    case "error":
      return "bg-rose-50 text-rose-700 border-rose-200";
    default:
      return "bg-slate-50 text-slate-600 border-slate-200";
  }
};

export default function HealthCard({ title, status, children }: Props) {
  return (
    <div
      className={clsx(
        "rounded-lg border p-4 shadow-sm",
        statusColor(status)
      )}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-semibold">{title}</h3>
        <span className="text-xs uppercase tracking-wide">
          {status}
        </span>
      </div>

      <div className="text-xs space-y-1">{children}</div>
    </div>
  );
}
