import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  output: 'static',
  integrations: [react(), tailwind()],
  site: 'https://16s893-ai-for-engineering-research.github.io/annarich00',
  base: '/annarich00/',
});
