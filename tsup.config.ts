import { copyFileSync } from "node:fs";

import { defineConfig } from "tsup";

export default defineConfig({
  entry: { index: "src/index.ts", "tailwind.preset": "src/tailwind.preset.ts" },
  format: ["esm", "cjs"],
  dts: true,
  clean: true,
  sourcemap: true,
  // Copy the raw CSS verbatim — it isn't bundled, consumers import it directly.
  onSuccess: async () => {
    copyFileSync("src/css/variables.css", "dist/variables.css");
    copyFileSync("src/css/reset.css", "dist/reset.css");
  },
});
