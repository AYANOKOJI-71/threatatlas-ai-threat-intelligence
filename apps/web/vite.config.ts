import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const apiOrigin = process.env.THREATATLAS_API_ORIGIN ?? "http://127.0.0.1:4910";

export default defineConfig({
  plugins: [react()],
  server: {
    allowedHosts: [".manus.computer"],
    proxy: {
      "/api": apiOrigin,
      "/health": apiOrigin,
      "/metrics": apiOrigin
    }
  }
});
