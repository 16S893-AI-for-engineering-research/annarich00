import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  output: 'static',
  integrations: [react(), tailwind()],
  site: 'https://annarich.github.io/agent_retry',
  base: '/agent_retry/',
});
