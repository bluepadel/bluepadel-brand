import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist/**", "node_modules/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  // Node scripts (generators, sync) run under node — give them node globals.
  {
    files: ["scripts/**/*.{mjs,cjs,js}"],
    languageOptions: {
      globals: { process: "readonly", console: "readonly" },
    },
  },
);
