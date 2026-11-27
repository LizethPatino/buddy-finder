/**
 * Vite configuration for the Buddy Finder frontend.
 * Configures React support for local development
 * and production builds.
 */

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
})