import { describe, expect, it } from "vitest";

import { dark, light, palette, radius, semantic, shadow, spacing, typography } from "../src/index";
import preset from "../src/tailwind.preset";

describe("bluepadel-brand tokens", () => {
  it("exposes the brand primary", () => {
    expect(palette.blue[800]).toBe("#1565C0");
  });

  it("has a complete blue + neutral ramp", () => {
    for (const k of [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]) {
      expect(palette.blue[k as keyof typeof palette.blue]).toMatch(/^#[0-9A-Fa-f]{6}$/);
      expect(palette.neutral[k as keyof typeof palette.neutral]).toMatch(/^#[0-9A-Fa-f]{6}$/);
    }
  });

  it("semantic tokens reference CSS vars, never raw hex", () => {
    const values = Object.values(semantic.color);
    expect(values.length).toBeGreaterThan(0);
    for (const v of values) {
      expect(v).toMatch(/^var\(--bp-color-/);
      expect(v).not.toMatch(/#[0-9A-Fa-f]{3,6}/);
    }
  });

  it("scales are present", () => {
    expect(typography.fontSize.base[0]).toBe("1rem");
    expect(typography.fontSize["display-xl"][0]).toBe("8rem");
    expect(spacing[4]).toBe("1rem");
    expect(radius.md).toBe("0.5rem");
    expect(shadow.md).toContain("rgba");
  });

  it("tailwind preset binds colours to semantic vars", () => {
    const colors = preset.theme?.extend?.colors as Record<string, unknown>;
    expect(colors.surface).toBe("var(--bp-color-surface)");
    expect((colors.primary as Record<string, string>).DEFAULT).toBe("var(--bp-color-primary)");
  });

  // themes.ts is the resolved (hex) twin of css/variables.css, consumed by the
  // non-CSS generators (Android/Compose). Keep it tied to the palette so it
  // can't drift back to an off-brand primary like the old Android #1E40AF.
  it("themes resolve to the brand palette (light + dark)", () => {
    expect(light.primary).toBe(palette.blue[800]); // brand #1565C0
    expect(light.bg).toBe(palette.neutral[50]);
    expect(light.textMuted).toBe(palette.neutral[500]);
    expect(dark.primary).toBe(palette.blue[400]); // brightened for dark
    expect(dark.surface).toBe("#111C2E");
    // Every semantic value is a concrete hex or rgba — never a CSS var.
    for (const v of [...Object.values(light), ...Object.values(dark)]) {
      if (typeof v === "string") expect(v).toMatch(/^(#[0-9A-Fa-f]{6}|rgba?\()/);
    }
  });
});
