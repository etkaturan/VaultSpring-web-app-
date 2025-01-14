/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'], // Adjust paths as needed
  theme: {
      extend: {
        colors: {
          'custom-blue': 'rgb(87,135,218)',
      },
      }, // Add customizations if required
  },
  variants: {
    extend: {
        scale: ['group-hover'], // Enable group-hover for scale
    },
},
  plugins: [],
};