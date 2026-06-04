/** PRIMITIVE elevation scale (cast from neutral-900 at low alpha). */
export const shadow = {
  none: "none",
  sm: "0 1px 2px rgba(11,19,32,0.06)",
  md: "0 4px 8px rgba(11,19,32,0.10)",
  lg: "0 12px 24px rgba(11,19,32,0.12)",
  xl: "0 24px 48px rgba(11,19,32,0.16)",
  inner: "inset 0 2px 4px rgba(11,19,32,0.05)",
} as const;

export type Shadow = typeof shadow;
