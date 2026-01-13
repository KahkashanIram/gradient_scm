// frontend/types/admin.ts

export interface AdminActivityLog {
    id: number;
    admin_user: string;
    action: string;
    module: string;
    object_id: string | null;
    ip_address: string | null;
    created_at: string;
    metadata: Record<string, string | number | boolean | null>;
  }
  
  export interface AdminActivityLogResponse {
    count: number;
    next: string | null;
    previous: string | null;
    results: AdminActivityLog[];
  }
  