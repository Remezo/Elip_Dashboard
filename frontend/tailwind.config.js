/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Ascentris brand colors
        brand: {
          black: "#1a1a1a",
          charcoal: "#2d2d2d",
          dark: "#3a3a3a",
          gray: "#4a4a4a",
          muted: "#6b6b6b",
          light: "#a0a0a0",
          gold: "#c8a84e",
          "gold-light": "#d4b85c",
          "gold-dark": "#b89a3e",
          white: "#f5f5f5",
        },
      },
    },
  },
  plugins: [],
};
