// frontend/lib/safe.ts

export function asString(
    value: unknown,
    fallback = "-"
  ): string {
    return typeof value === "string" ? value : fallback;
  }
  
  export function asNumber(
    value: unknown,
    fallback = "-"
  ): string {
    return typeof value === "number" ? value.toString() : fallback;
  }
  