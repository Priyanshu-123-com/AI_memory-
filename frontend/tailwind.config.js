/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                obsidian: "#050505",
                neon: {
                    cyan: "#00F2FF",
                    blue: "#2E7CFF", // Adjusted for Matrix
                    teal: "#00C2CB", // Semantic
                    amber: "#FFB800", // Graph
                }
            },
            fontFamily: {
                mono: ['"JetBrains Mono"', "monospace"],
                sans: ['"Inter"', "sans-serif"],
            },
            animation: {
                'pulse-fast': 'pulse 1s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            }
        },
    },
    plugins: [],
}
