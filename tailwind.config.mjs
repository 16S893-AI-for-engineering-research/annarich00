/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        void: '#050816',
        orbital: '#79f2ff',
        thruster: '#ffb347',
      },
      boxShadow: {
        glow: '0 0 40px rgba(121, 242, 255, 0.16)',
      },
    },
  },
  plugins: [],
};
