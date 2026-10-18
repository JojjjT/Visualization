# Equipo 7 · Proyecto 2 · Recetas de bienestar (WHR 2024)

**Joshua Trujillo y Nicolás Figueroa**  
Visualización I · Universidad Externado de Colombia · Octubre 2026

Análisis reproducible del *World Happiness Report 2024*: qué combinaciones de indicadores se asocian con mayor o menor evaluación de vida, y cómo el componente no explicado (Distopía + residual) matiza esas «recetas».

> Todo el análisis muestra **asociaciones**, no causalidad.

---

## Sitio en vivo (GitHub Pages)

| Página | URL |
|--------|-----|
| Inicio | https://jojjjt.github.io/Visualization/ |
| Gráficos Plotly | https://jojjjt.github.io/Visualization/Equipo7_Proyecto2_Interactivos.html |
| Notebook Marimo (WASM) | https://jojjjt.github.io/Visualization/wasm/ |

Si Pages aún no está activo: **Settings → Pages → Source: GitHub Actions**.

---

## Pregunta analítica

¿Qué «recetas» de bienestar predominan entre los países con mayor y menor evaluación de vida según el WHR 2024, y en qué medida el componente no explicado (Distopía + residual) altera o cuestiona dichas recetas?

**Audiencia:** unidad de investigación comparativa (p. ej. PNUD / Banco Mundial).

---

## Hallazgos clave

1. Los terciles superior e inferior comparten la misma **estructura** de receta (PIB ≈ 34–35 % y apoyo social ≈ 27–29 % concentran > 60 %). La diferencia es de **nivel**.
2. El residual \(D\) varía de −0,07 a 3,00 y se asocia con \(L\) (r ≈ 0,53). Seis de los diez países con mayor \(D\) son latinoamericanos.
3. Atípicos: 1 alto (Venezuela) y 5 bajos (mayormente tercil inferior).

---

## Estructura del repositorio

```
.
├── .github/workflows/pages.yml      # Build WASM + deploy a Pages
├── notebooks/
│   └── Equipo7_Proyecto2_Marimo.py  # Notebook (matplotlib + plotly)
├── public/
│   └── whr24.csv                   # Datos WHR 2024 preparados
├── Equipo7_Proyecto2_Interactivos.html
├── index.html
└── README.md
```

---

## Cómo se publica

Cada push a `main` ejecuta el workflow:

1. Ubuntu + Python 3.12 + marimo
2. `marimo export html-wasm` del notebook
3. Despliegue del sitio estático a GitHub Pages

No hace falta generar el WASM en local.

---

## Notas técnicas

- El notebook Marimo **no usa seaborn** (no está en el canal por defecto de Pyodide). Figuras estáticas con **matplotlib**; interactivas con **plotly**.
- El HTML de Plotly no depende de WASM y funciona siempre.
- Fuente de datos: *World Happiness Report 2024*, Data for Figure 2.1.

---

## Entregables del curso

Además de este sitio, el paquete del Proyecto 2 incluye:

- Notebook Jupyter (Seaborn + Plotly, reproducible)
- Resumen PDF (≤ 3 páginas)
- Anexo de uso de IA
- `requirements.txt` y datos originales
