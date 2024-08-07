import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    proxy: {
      // 代理配置
      '/api': {
        target: 'http://localhost:3000', // 确保这里的地址是你的后端服务地址
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
});