// frontend/types/system.ts

export type HealthStatus = "ok" | "warning" | "error" | "unknown";

/* ---------- Detail Types ---------- */

export interface ApplicationDetails {
  service: string;
}

export interface DatabaseDetails {
  engine: string;
}

export interface SystemDetails {
  cpu_percent: number;
  memory_percent: number;
  memory_total_mb: number;
  memory_available_mb: number;
  disk_percent: number;
  disk_total_gb: number;
  disk_free_gb: number;
}

/* ---------- Component Wrapper ---------- */

export interface HealthComponent<TDetails> {
  status: HealthStatus;
  details: TDetails;
}

/* ---------- API Response ---------- */

export interface SystemHealthResponse {
  status: HealthStatus;
  timestamp: string;
  components: {
    application: HealthComponent<ApplicationDetails>;
    database: HealthComponent<DatabaseDetails>;
    system: HealthComponent<SystemDetails>;
  };
}
