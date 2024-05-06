/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'mint': {
          100: '#3EB489'
        },
        'seawater': {
          100: '#76b6c4',
          400: '#b4d2d3'
        },
        'darkgray': {
          800: '#202020',
          400: '#404040'
        }
      },
    },
  },
  plugins: [
    require('tailwind-scrollbar'),
    require('tailwind-scrollbar-hide'),
  ],
}

