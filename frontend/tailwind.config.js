/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'sans-serif'],
                display: ['Inter', 'ui-sans-serif', 'sans-serif'],
            },
            colors: {
                primary: {
                    50: '#f0fdf4',
                    100: '#dcfce7',
                    200: '#bbf7d0',
                    300: '#86efac',
                    400: '#4ade80',
                    500: '#22c55e',
                    600: '#16a34a',
                    700: '#15803d',
                    800: '#166534',
                    900: '#14532d',
                },
                sport: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    500: '#0ea5e9',
                    600: '#0284c7',
                    700: '#0369a1',
                },
                brand: {
                    primary: '#ff007f',
                    secondary: '#00f3ff',
                    accent: '#ccff00',
                }
            },
            boxShadow: {
                'card': '0 1px 3px 0 rgba(0,0,0,0.06), 0 1px 2px -1px rgba(0,0,0,0.06)',
                'card-hover': '0 4px 12px -2px rgba(0,0,0,0.10), 0 2px 6px -2px rgba(0,0,0,0.06)',
                'btn': '0 1px 2px 0 rgba(0,0,0,0.08)',
                'luxury': '0 10px 40px -10px rgba(0, 0, 0, 0.9), 0 1px 1px rgba(255, 255, 255, 0.1) inset, 0 0 15px rgba(255, 0, 127, 0.15)',
                'glow': '0 0 50px rgba(0, 243, 255, 0.4)',
            },
            borderRadius: {
                'xl2': '1rem',
                'xl3': '1.25rem',
            },
            animation: {
                'strobe': 'strobeFloat 12s infinite alternate cubic-bezier(0.4, 0, 0.2, 1)',
            }
        },
    },
    plugins: [],
}
