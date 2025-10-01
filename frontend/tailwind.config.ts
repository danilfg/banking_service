import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#0B5FFF',
        secondary: '#111827',
        accent: '#00C48C'
      }
    }
  },
  plugins: []
};

export default config;
