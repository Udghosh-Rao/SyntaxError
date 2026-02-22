/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            colors: {
                brand: {
                    primary: '#ff007f',
                    secondary: '#00f3ff',
                    accent: '#ccff00',
                }
            }
        },
    },
    plugins: [],
}
