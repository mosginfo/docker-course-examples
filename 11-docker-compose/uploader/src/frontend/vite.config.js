import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const proxyDefaults = {
  target: 'http://backend:5000',
  changeOrigin: true,
}

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        ...proxyDefaults,
        rewrite: path => path.replace(/^\/api/, ''),
      },
      '/media': proxyDefaults,
    },
  },
})

