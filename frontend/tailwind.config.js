/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef4ff",
          100: "#dbe7ff",
          500: "#3157a4",
          600: "#24498e",
          700: "#19366d"
        }
      }
    }
  },
  plugins: []
}
