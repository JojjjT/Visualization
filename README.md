# Equipo 7 · Proyecto 2 · Recetas de bienestar (WHR 2024)

Joshua Trujillo y Nicolás Figueroa · Visualización I · Universidad Externado de Colombia

## Estructura del repositorio

```
.
├── .github/workflows/pages.yml   # Build Marimo WASM + deploy Pages
├── notebooks/
│   └── Equipo7_Proyecto2_Marimo.py
├── public/
│   └── whr24.csv
├── Equipo7_Proyecto2_Interactivos.html
├── index.html
└── README.md
```

## Activar GitHub Pages

1. Sube este contenido a un repo (branch `main`).
2. **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Cada push a `main` ejecuta el workflow, exporta el notebook a WASM y publica el sitio.

URLs típicas:

- `https://USER.github.io/REPO/` — inicio
- `https://USER.github.io/REPO/Equipo7_Proyecto2_Interactivos.html` — Plotly
- `https://USER.github.io/REPO/wasm/` — Marimo WASM

## Notas

- El notebook Marimo **no usa seaborn** (no está en el canal por defecto de Pyodide). Las figuras estáticas van con matplotlib; las interactivas con plotly.
- El HTML de Plotly no depende de WASM y funciona siempre.
- No hace falta instalar nada en Windows para el WASM: lo construye Actions en Ubuntu.
