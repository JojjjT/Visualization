"""
Recetas de bienestar — WHR 2024 (WASM)
Equipo 7 · Joshua Trujillo y Nicolás Figueroa
Solo matplotlib + pandas (compatibles con Pyodide).
Plotly interactivo: Equipo7_Proyecto2_Interactivos.html
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
    return C, COLORES, ETIQUETA, ORDEN_TERCIL, mo, np, pd, pathlib, plt


@app.cell
def _(mo):
    mo.md(
        r"""
        # Recetas de bienestar: ¿qué explican (y qué no) los seis indicadores del WHR 2024?

        **Equipo 7:** Joshua Trujillo y Nicolás Figueroa · Visualización I · Universidad Externado de Colombia

        **Pregunta.** ¿Qué «recetas» de bienestar predominan entre los países con mayor y menor evaluación de vida, y en qué medida el componente no explicado ($D$) las cuestiona?

        > Asociaciones, no causalidad.

        Los gráficos **interactivos** (Plotly) están en
        [Equipo7_Proyecto2_Interactivos.html](../Equipo7_Proyecto2_Interactivos.html).
        """
    )
    return


@app.cell
def _(mo, pathlib, pd):
    _base = pathlib.Path(str(mo.notebook_location())) if hasattr(mo, "notebook_location") else pathlib.Path(".")
    _candidates = [
        _base / "public" / "whr24.csv",
        pathlib.Path("public") / "whr24.csv",
        _base.parent / "public" / "whr24.csv",
    ]
    csv_path = next((p for p in _candidates if p.exists()), None)
    if csv_path is None:
        raise FileNotFoundError("No se encontró public/whr24.csv")
    df = pd.read_csv(csv_path)
    mo.md(f"**Datos:** {len(df)} países · `{csv_path.name}`")
    return (df,)


@app.cell
def _(C, ORDEN_TERCIL, df, mo, np, pd):
    df2 = df.copy()
    df2["tercil"] = pd.qcut(df2["L"], q=3, labels=ORDEN_TERCIL)
    df2["suma_explicada"] = df2[C].sum(axis=1, skipna=False)
    completos = df2.dropna(subset=C + ["D"]).copy()

    _q1, _q3 = completos["D"].quantile([0.25, 0.75])
    _riq = _q3 - _q1
    lim_inf = float(_q1 - 1.5 * _riq)
    lim_sup = float(_q3 + 1.5 * _riq)
    completos["atipico_D"] = np.select(
        [completos["D"] > lim_sup, completos["D"] < lim_inf],
        ["Alto", "Bajo"],
        default="No",
    )
    cortes = df2["L"].quantile([1 / 3, 2 / 3]).values
    _excluidos = sorted(set(df2["pais"]) - set(completos["pais"]))

    mo.md(
        f"""
        ## Preparación

        | Indicador | Valor |
        |---|---|
        | Países totales | {len(df2)} |
        | Con receta completa | {len(completos)} |
        | Excluidos | {", ".join(_excluidos)} |
        | Cortes terciles de $L$ | {cortes[0]:.2f}, {cortes[1]:.2f} |
        | Límites Tukey de $D$ | [{lim_inf:.2f}, {lim_sup:.2f}] |
        | Atípicos $D$ | {completos["atipico_D"].value_counts().to_dict()} |
        """
    )
    return completos, cortes, df2, lim_inf, lim_sup


@app.cell
def _(completos, cortes, df2, plt):
    fig_hist, axes_hist = plt.subplots(1, 2, figsize=(10, 3.8))
    axes_hist[0].hist(df2["L"].dropna(), bins=20, color="#0072B2", edgecolor="white", alpha=0.9)
    for _c in cortes:
        axes_hist[0].axvline(_c, color="black", ls="--", lw=1)
    axes_hist[0].set_title("Ladder score L (143 países)")
    axes_hist[0].set_xlabel("L")
    axes_hist[0].set_ylabel("Países")

    axes_hist[1].hist(completos["D"].dropna(), bins=20, color="#009E73", edgecolor="white", alpha=0.9)
    axes_hist[1].axvline(completos["D"].median(), color="black", ls="--", lw=1)
    axes_hist[1].set_title(f"Componente no explicado D ({len(completos)} países)")
    axes_hist[1].set_xlabel("D")
    plt.tight_layout()
    fig_hist
    return


@app.cell
def _(C, COLORES, ETIQUETA, ORDEN_TERCIL, completos, plt):
    fig_box, axes_box = plt.subplots(2, 3, figsize=(11, 6))
    _flat = axes_box.ravel()
    for _idx, _col in enumerate(C):
        _data = [completos.loc[completos["tercil"] == _t, _col].dropna().values for _t in ORDEN_TERCIL]
        _bp = _flat[_idx].boxplot(_data, tick_labels=ORDEN_TERCIL, patch_artist=True)
        for _patch, _t in zip(_bp["boxes"], ORDEN_TERCIL):
            _patch.set_facecolor(COLORES[_t])
            _patch.set_alpha(0.8)
        _flat[_idx].set_title(ETIQUETA[_col], fontsize=9)
        _flat[_idx].tick_params(labelsize=8)
    fig_box.suptitle("Indicadores por tercil de bienestar", fontsize=12)
    plt.tight_layout()
    fig_box
    return


@app.cell
def _(C, COLORES, ETIQUETA, ORDEN_TERCIL, completos, plt):
    _absolutos = completos.groupby("tercil", observed=True)[C].mean()
    fig_bar, ax_bar = plt.subplots(figsize=(9, 4.5))
    _x = list(range(len(C)))
    _w = 0.25
    for _i, _t in enumerate(ORDEN_TERCIL):
        _vals = [_absolutos.loc[_t, _c] for _c in C]
        ax_bar.bar([_xi + _i * _w for _xi in _x], _vals, width=_w, label=_t, color=COLORES[_t])
    ax_bar.set_xticks([_xi + _w for _xi in _x])
    ax_bar.set_xticklabels([ETIQUETA[_c] for _c in C], rotation=25, ha="right", fontsize=8)
    ax_bar.set_ylabel("Aporte medio (puntos)")
    ax_bar.set_title("Perfil de receta por tercil")
    ax_bar.legend()
    plt.tight_layout()
    fig_bar
    return


@app.cell
def _(COLORES, ORDEN_TERCIL, completos, lim_inf, lim_sup, plt):
    r = float(completos[["L", "D"]].corr().iloc[0, 1])
    fig_sc, ax_sc = plt.subplots(figsize=(9, 5))
    for _t in ORDEN_TERCIL:
        _s = completos[completos["tercil"] == _t]
        ax_sc.scatter(
            _s["L"], _s["D"], c=COLORES[_t], label=f"Tercil {_t}",
            s=40, alpha=0.85, edgecolors="white", linewidths=0.4,
        )
    ax_sc.axhline(completos["D"].median(), color="black", ls="--", lw=1)
    ax_sc.axhspan(lim_inf, lim_sup, color="grey", alpha=0.1)
    ax_sc.set_xlabel("Ladder score L")
    ax_sc.set_ylabel("D (Distopía + residual)")
    ax_sc.set_title(f"D frente a L (r = {r:.2f})")
    ax_sc.legend()
    plt.tight_layout()
    fig_sc
    return (r,)


@app.cell
def _(mo, r):
    mo.md(
        rf"""
        ## Conclusiones

        1. **Recetas.** Misma estructura (PIB ≈34–35 %, apoyo social ≈27–29 % > 60 %). Diferencia de **nivel**.
        2. **Componente no explicado.** $D$ de −0,07 a 3,00; r($L$,$D$) ≈ {r:.2f}. Seis de los diez mayores $D$ son latinoamericanos.
        3. **Atípicos.** 1 alto (Venezuela), 5 bajos (mayormente tercil inferior).
        4. **Limitaciones.** Asociaciones, no causalidad; $D$ mezcla Distopía y residual.

        Gráficos interactivos (Plotly): [Equipo7_Proyecto2_Interactivos.html](../Equipo7_Proyecto2_Interactivos.html)

        ---
        *Equipo 7 · WHR 2024 · Visualización I · Universidad Externado de Colombia*
        """
    )
    return


if __name__ == "__main__":
    app.run()
