"""
Recetas de bienestar — WHR 2024
Equipo 7 · Joshua Trujillo y Nicolás Figueroa
Visualización I · Universidad Externado de Colombia

Notebook Marimo orientado a export WASM (GitHub Actions / Pages).
Usa matplotlib + plotly (sin seaborn: no está en el canal por defecto de Pyodide).
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Equipo 7 · Recetas de bienestar WHR 2024")


@app.cell
def _():
    import pathlib
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    import marimo as mo

    pd.set_option("display.precision", 2)

    ORDEN_TERCIL = ["Inferior", "Medio", "Superior"]
    COLORES = {"Inferior": "#D55E00", "Medio": "#999999", "Superior": "#0072B2"}
    C = ["c_PIB", "c_social", "c_vida", "c_libertad", "c_generosidad", "c_corrupcion"]
    ETIQUETA = {
        "c_PIB": "PIB per cápita (log)",
        "c_social": "Apoyo social",
        "c_vida": "Esperanza de vida saludable",
        "c_libertad": "Libertad para decidir",
        "c_generosidad": "Generosidad",
        "c_corrupcion": "Percepción de corrupción",
    }
    return C, COLORES, ETIQUETA, ORDEN_TERCIL, go, mo, np, pd, pathlib, plt


@app.cell
def _(mo):
    mo.md(
        r"""
        # Recetas de bienestar: ¿qué explican (y qué no) los seis indicadores del World Happiness Report 2024?

        **Proyecto 2 · Visualización reproducible** · Visualización I · Universidad Externado de Colombia  
        **Equipo 7:** Joshua Trujillo y Nicolás Figueroa · Octubre de 2026

        **Audiencia.** Unidad de investigación comparativa (p. ej. PNUD / Banco Mundial).

        **Pregunta.** ¿Qué «recetas» de bienestar predominan entre los países con mayor y menor evaluación de vida según el WHR 2024, y en qué medida el componente no explicado (Distopía + residual) altera o cuestiona dichas recetas?

        **Subpreguntas**
        1. ¿Qué combinación de los seis indicadores caracteriza a los terciles superior e inferior?
        2. ¿Qué países presentan el componente $D_i$ más alto y qué tienen en común?
        3. ¿Los atípicos concentran residuales elevados o reducidos?

        > **Advertencia.** Todo lo mostrado son **asociaciones**, no causalidad.
        """
    )
    return


@app.cell
def _(mo, pathlib, pd):
    base = pathlib.Path(str(mo.notebook_location())) if hasattr(mo, "notebook_location") else pathlib.Path(".")
    candidates = [
        base / "public" / "whr24.csv",
        pathlib.Path("public") / "whr24.csv",
        base.parent / "public" / "whr24.csv",
    ]
    csv_path = next((p for p in candidates if p.exists()), None)
    if csv_path is None:
        raise FileNotFoundError(
            "No se encontró public/whr24.csv. "
            "En el repo debe existir public/whr24.csv junto al notebook o en la raíz del sitio."
        )
    df = pd.read_csv(csv_path)
    mo.md(f"**Datos cargados:** {len(df)} países · `{csv_path.name}`")
    return (df,)


@app.cell
def _(C, ORDEN_TERCIL, df, mo, np, pd):
    df2 = df.copy()
    df2["tercil"] = pd.qcut(df2["L"], q=3, labels=ORDEN_TERCIL)
    df2["suma_explicada"] = df2[C].sum(axis=1, skipna=False)
    completos = df2.dropna(subset=C + ["D"]).copy()

    q1, q3 = completos["D"].quantile([0.25, 0.75])
    riq = q3 - q1
    lim_inf, lim_sup = q1 - 1.5 * riq, q3 + 1.5 * riq
    completos["atipico_D"] = np.select(
        [completos["D"] > lim_sup, completos["D"] < lim_inf],
        ["Alto", "Bajo"],
        default="No",
    )
    cortes = df2["L"].quantile([1 / 3, 2 / 3]).values
    excluidos = sorted(set(df2["pais"]) - set(completos["pais"]))

    mo.md(
        f"""
        ## Preparación

        | Indicador | Valor |
        |---|---|
        | Países totales | {len(df2)} |
        | Con receta completa | {len(completos)} |
        | Excluidos | {", ".join(excluidos)} |
        | Cortes terciles de $L$ | {cortes[0]:.2f}, {cortes[1]:.2f} |
        | Límites Tukey de $D$ | [{lim_inf:.2f}, {lim_sup:.2f}] |
        | Atípicos $D$ | {completos["atipico_D"].value_counts().to_dict()} |
        """
    )
    return completos, cortes, df2, lim_inf, lim_sup


@app.cell
def _(completos, cortes, df2, plt):
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    ax[0].hist(df2["L"].dropna(), bins=20, color="#0072B2", edgecolor="white", alpha=0.9)
    for c in cortes:
        ax[0].axvline(c, color="black", ls="--", lw=1)
    ax[0].set_title("Ladder score L (143 países)")
    ax[0].set_xlabel("L")
    ax[0].set_ylabel("Países")

    ax[1].hist(completos["D"].dropna(), bins=20, color="#009E73", edgecolor="white", alpha=0.9)
    ax[1].axvline(completos["D"].median(), color="black", ls="--", lw=1)
    ax[1].set_title(f"Componente no explicado D ({len(completos)} países)")
    ax[1].set_xlabel("D")
    plt.tight_layout()
    fig
    return


@app.cell
def _(C, COLORES, ETIQUETA, ORDEN_TERCIL, completos, plt):
    fig, axes = plt.subplots(2, 3, figsize=(11, 6))
    axes = axes.ravel()
    for i, col in enumerate(C):
        data = [completos.loc[completos["tercil"] == t, col].dropna().values for t in ORDEN_TERCIL]
        bp = axes[i].boxplot(data, tick_labels=ORDEN_TERCIL, patch_artist=True)
        for patch, t in zip(bp["boxes"], ORDEN_TERCIL):
            patch.set_facecolor(COLORES[t])
            patch.set_alpha(0.8)
        axes[i].set_title(ETIQUETA[col], fontsize=9)
        axes[i].tick_params(labelsize=8)
    fig.suptitle("Indicadores por tercil de bienestar", fontsize=12)
    plt.tight_layout()
    fig
    return


@app.cell
def _(C, COLORES, ETIQUETA, ORDEN_TERCIL, completos, plt):
    absolutos = completos.groupby("tercil", observed=True)[C].mean()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    x = list(range(len(C)))
    w = 0.25
    for i, t in enumerate(ORDEN_TERCIL):
        vals = [absolutos.loc[t, c] for c in C]
        ax.bar([xi + i * w for xi in x], vals, width=w, label=t, color=COLORES[t])
    ax.set_xticks([xi + w for xi in x])
    ax.set_xticklabels([ETIQUETA[c] for c in C], rotation=25, ha="right", fontsize=8)
    ax.set_ylabel("Aporte medio (puntos)")
    ax.set_title("Perfil de receta por tercil")
    ax.legend()
    plt.tight_layout()
    fig
    return


@app.cell
def _(COLORES, ORDEN_TERCIL, completos, lim_inf, lim_sup, plt):
    r = float(completos[["L", "D"]].corr().iloc[0, 1])
    fig, ax = plt.subplots(figsize=(9, 5))
    for t in ORDEN_TERCIL:
        s = completos[completos["tercil"] == t]
        ax.scatter(
            s["L"], s["D"], c=COLORES[t], label=f"Tercil {t}",
            s=40, alpha=0.85, edgecolors="white", linewidths=0.4,
        )
    ax.axhline(completos["D"].median(), color="black", ls="--", lw=1)
    ax.axhspan(lim_inf, lim_sup, color="grey", alpha=0.1)
    ax.set_xlabel("Ladder score L")
    ax.set_ylabel("D (Distopía + residual)")
    ax.set_title(f"D frente a L (r = {r:.2f})")
    ax.legend()
    plt.tight_layout()
    fig
    return (r,)


@app.cell
def _(C, COLORES, ORDEN_TERCIL, completos, go, np):
    d_medio = float(completos["D"].mean())
    size_vals = completos["D"].clip(lower=0.05)
    sizeref = 2.0 * float(size_vals.max()) / (34.0 ** 2)

    fig_p1 = go.Figure()
    for t in ORDEN_TERCIL:
        s = completos[completos["tercil"] == t]
        fig_p1.add_trace(
            go.Scatter(
                x=s["suma_explicada"],
                y=s["L"],
                mode="markers",
                name=f"Tercil {t}",
                marker=dict(
                    color=COLORES[t],
                    size=s["D"].clip(lower=0.05),
                    sizemode="area",
                    sizeref=sizeref,
                    line=dict(color="white", width=0.6),
                    opacity=0.85,
                ),
                text=s["pais"],
                hovertemplate="<b>%{text}</b><br>L=%{y:.2f} · Σc=%{x:.2f}<extra></extra>",
            )
        )
    xr = np.array([completos["suma_explicada"].min(), completos["suma_explicada"].max()])
    fig_p1.add_trace(
        go.Scatter(
            x=xr,
            y=xr + d_medio,
            mode="lines",
            name="L = Σc + D medio",
            line=dict(color="black", dash="dash", width=1),
            hoverinfo="skip",
        )
    )
    fig_p1.update_layout(
        title="Receta explicada vs evaluación de vida (tamaño = D)",
        xaxis_title="Suma de las seis contribuciones Σc",
        yaxis_title="Ladder score L",
        template="plotly_white",
        height=520,
    )
    fig_p1
    return


@app.cell
def _(COLORES, ETIQUETA, ORDEN_TERCIL, completos, go, np):
    fig_p2 = go.Figure()
    orden_paises = {}
    for col, etiqueta in ETIQUETA.items():
        top = completos.nlargest(15, col).sort_values(col)
        orden_paises[col] = list(top["pais"])
        fig_p2.add_trace(
            go.Bar(
                x=top[col],
                y=top["pais"],
                orientation="h",
                showlegend=False,
                marker_color=[COLORES[t] for t in top["tercil"]],
                visible=(col == "c_PIB"),
                customdata=np.c_[top["tercil"].astype(str), top["L"]],
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    + etiqueta
                    + ": %{x:.2f}<br>Tercil: %{customdata[0]} · L=%{customdata[1]:.2f}<extra></extra>"
                ),
            )
        )
    for t in ORDEN_TERCIL:
        fig_p2.add_trace(
            go.Bar(x=[None], y=[None], orientation="h", name=f"Tercil {t}", marker_color=COLORES[t])
        )
    n_ind = len(ETIQUETA)
    botones = []
    for i, (col, etiqueta) in enumerate(ETIQUETA.items()):
        botones.append(
            dict(
                label=etiqueta,
                method="update",
                args=[
                    {"visible": [j == i for j in range(n_ind)] + [True] * 3},
                    {
                        "title": f"Top 15 países en: {etiqueta}",
                        "xaxis.title": f"Contribución — {etiqueta}",
                        "yaxis.categoryarray": orden_paises[col],
                    },
                ],
            )
        )
    fig_p2.update_layout(
        title="Top 15 países en: " + ETIQUETA["c_PIB"],
        template="plotly_white",
        height=560,
        xaxis_title=f"Contribución — {ETIQUETA['c_PIB']}",
        yaxis=dict(categoryorder="array", categoryarray=orden_paises["c_PIB"]),
        updatemenus=[dict(type="dropdown", buttons=botones, x=0.0, xanchor="left", y=1.12, yanchor="top")],
        legend_title="Tercil de bienestar",
    )
    fig_p2
    return


@app.cell
def _(mo, r):
    mo.md(
        rf"""
        ## Conclusiones

        1. **Recetas.** Los terciles superior e inferior comparten estructura: PIB (≈34–35 %) y apoyo social (≈27–29 %) concentran más del 60 %. La diferencia es de **nivel**.
        2. **Componente no explicado.** $D$ va de −0,07 a 3,00; se asocia con $L$ (r ≈ {r:.2f}). Seis de los diez países con mayor $D$ son latinoamericanos.
        3. **Atípicos.** Un alto (Venezuela) y cinco bajos (mayormente tercil inferior).
        4. **Limitaciones.** Asociaciones (no causalidad); $D$ mezcla Distopía y residual; terciles relativos a esta muestra; datos Gallup 2021–2023.

        ---
        *Equipo 7 · Proyecto 2 · Visualización I · Universidad Externado de Colombia*  
        Fuente: World Happiness Report 2024, Data for Figure 2.1
        """
    )
    return


if __name__ == "__main__":
    app.run()
