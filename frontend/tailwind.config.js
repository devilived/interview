/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#F8FAFC',
        card: '#FFFFFF',
        text: '#1E293B',
        accent: '#475569',
        'accent-green': '#059669'
      }
    },
  },
  plugins: [],
}
