import { fileURLToPath, URL } from 'node:url';
import Components from 'unplugin-vue-components/vite';
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { version } from './package.json';

// https://vitejs.dev/config/
export default defineConfig({
  define: {
    __VERSION__: `'${version}'`,
  },
  plugins: [
    vue(),
    Components({
      resolvers: [
        AntDesignVueResolver(),
      ],
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 8080,
    proxy: {
      '/api': 'http://127.0.0.1:2023',
    },
  }
});
