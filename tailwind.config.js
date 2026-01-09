/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // We handle dark mode manually in React state
  content: [
    "./app/**/*.{js,jsx,mdx}",
    "./components/**/*.{js,jsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['var(--font-crimson)', 'serif'],
      },
    },
  },
  plugins: [],
};