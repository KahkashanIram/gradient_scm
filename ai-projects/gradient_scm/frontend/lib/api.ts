// frontend/lib/api.ts

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL;

if (!API_BASE) {
  throw new Error(
    "NEXT_PUBLIC_BACKEND_URL is not defined. Check .env.local"
  );
}

/**
 * Central API fetcher for Django backend
 * - Uses session authentication (cookies)
 * - Safe default typing (unknown)
 */
export async function apiFetch<T = unknown>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    credentials: "include", // 🔐 Django session auth
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error ${response.status}`);
  }

  return response.json() as Promise<T>;
}
