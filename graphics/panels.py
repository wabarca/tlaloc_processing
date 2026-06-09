#!/usr/bin/env python3

import os

import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from graphics.basemap import draw_base
from graphics.colormaps import get_style

from core.dates import format_valid_time

from config.config import (
    FIGSIZE,
    DPI,
    PANEL_ROWS,
    PANEL_COLS,
    OPERATIONAL_DIR,
    UNCERTAINTY_DIR,
    PROBABILITY_DIR,
)

# =====================================================
# PRODUCT DEFINITIONS
# =====================================================

PRODUCT_DEFINITIONS = {
    "mean": {
        "title": "Mean",
        "style": "rain",
    },
    "median": {
        "title": "Median",
        "style": "rain",
    },
    "minimum": {
        "title": "Minimum",
        "style": "rain",
    },
    "maximum": {
        "title": "Maximum",
        "style": "rain",
    },
    "range": {
        "title": "Range",
        "style": "rain",
    },
    "spread": {
        "title": "Spread",
        "style": "spread",
    },
    "relative_spread": {
        "title": "Rel. Spread",
        "style": "relative_spread",
    },
    "p10": {
        "title": "P10",
        "style": "rain",
    },
    "p25": {
        "title": "P25",
        "style": "rain",
    },
    "p50": {
        "title": "P50",
        "style": "rain",
    },
    "p75": {
        "title": "P75",
        "style": "rain",
    },
    "p90": {
        "title": "P90",
        "style": "rain",
    },
    "prob_1": {
        "title": "P > 1 mm",
        "style": "prob",
    },
    "prob_10": {
        "title": "P > 10 mm",
        "style": "prob",
    },
    "prob_25": {
        "title": "P > 25 mm",
        "style": "prob",
    },
    "prob_50": {
        "title": "P > 50 mm",
        "style": "prob",
    },
    "prob_100": {
        "title": "P > 100 mm",
        "style": "prob",
    },
}

# =====================================================
# PANEL LAYOUTS
# =====================================================

PANEL_LAYOUTS = {
    "operational": [
        "mean",
        "median",
        "maximum",
        "prob_10",
        "prob_25",
        "prob_50",
        "spread",
        "relative_spread",
        "p90",
    ],
    "uncertainty": [
        "minimum",
        "maximum",
        "range",
        "p10",
        "p25",
        "p50",
        "p75",
        "p90",
        "spread",
    ],
    "probability": [
        "prob_1",
        "prob_10",
        "prob_25",
        "prob_50",
        "prob_100",
        "mean",
        "median",
        "p75",
        "p90",
    ],
}

# =====================================================
# PRODUCT ACCESS
# =====================================================


def get_product_data(
    products,
    product_name,
):
    """
    Devuelve el campo asociado
    a un producto.
    """

    if product_name in products:
        return products[product_name]

    if product_name.startswith("prob_"):

        threshold = int(product_name.split("_")[1])

        return products["probabilities"][threshold]

    if product_name.startswith("p"):

        percentile = int(product_name[1:])

        return products["percentiles"][percentile]

    raise KeyError(f"Producto no definido: " f"{product_name}")


# =====================================================
# PLOT
# =====================================================


def plot_product(
    ax,
    products,
    product_name,
    lon,
    lat,
):
    """
    Dibuja un producto en un subplot.

    Parameters
    ----------
    ax : GeoAxes

    products : dict

    product_name : str

    lon : ndarray

    lat : ndarray
    """

    # -----------------------------------------
    # Definición
    # -----------------------------------------

    definition = PRODUCT_DEFINITIONS[product_name]

    title = definition["title"]

    style = definition["style"]

    # -----------------------------------------
    # Datos
    # -----------------------------------------

    data = get_product_data(
        products,
        product_name,
    )

    # -----------------------------------------
    # Estilo
    # -----------------------------------------

    cmap, norm = get_style(style)

    # -----------------------------------------
    # Mapa base
    # -----------------------------------------

    draw_base(ax)

    # -----------------------------------------
    # Campo
    # -----------------------------------------

    mesh = ax.pcolormesh(
        lon,
        lat,
        data,
        cmap=cmap,
        norm=norm,
        transform=ccrs.PlateCarree(),
        shading="auto",
        rasterized=True,
    )

    # -----------------------------------------
    # Título
    # -----------------------------------------

    ax.set_title(
        title,
        fontsize=10,
        pad=4,
    )

    # -----------------------------------------
    # Colorbar
    # -----------------------------------------

    cbar = plt.colorbar(
        mesh,
        ax=ax,
        orientation="horizontal",
        pad=0.02,
        shrink=0.85,
        aspect=30,
    )

    cbar.ax.tick_params(labelsize=7)

    return mesh


# =====================================================
# PANEL
# =====================================================


def create_panel(
    products,
    lon,
    lat,
    timestep,
    panel_type,
):
    """
    Genera un panel completo.

    Parameters
    ----------
    products : dict

    lon : ndarray

    lat : ndarray

    timestep : int

    panel_type : str
        operational
        uncertainty
        probability
    """

    # -----------------------------------------
    # Layout
    # -----------------------------------------

    if panel_type not in PANEL_LAYOUTS:

        raise KeyError(f"Panel desconocido: " f"{panel_type}")

    layout = PANEL_LAYOUTS[panel_type]

    # -----------------------------------------
    # Figura
    # -----------------------------------------

    fig, axes = plt.subplots(
        PANEL_ROWS,
        PANEL_COLS,
        figsize=FIGSIZE,
        subplot_kw={"projection": ccrs.PlateCarree()},
    )

    axes = axes.flatten()

    # -----------------------------------------
    # Productos
    # -----------------------------------------

    for ax, product_name in zip(
        axes,
        layout,
    ):

        plot_product(
            ax=ax,
            products=products,
            product_name=product_name,
            lon=lon,
            lat=lat,
        )

    # -----------------------------------------
    # Título general
    # -----------------------------------------

    valid_time = format_valid_time(timestep)

    fig.suptitle(
        (
            "TLALOC Ensemble Forecast\n"
            f"Valid: {valid_time}\n"
            f"Lead Time: +{timestep:03d} h"
        ),
        fontsize=16,
        y=0.98,
    )

    # -----------------------------------------
    # Ajustes
    # -----------------------------------------

    plt.tight_layout(
        rect=[
            0,
            0,
            1,
            0.95,
        ]
    )

    # -----------------------------------------
    # Directorio
    # -----------------------------------------

    output_dirs = {
        "operational": OPERATIONAL_DIR,
        "uncertainty": UNCERTAINTY_DIR,
        "probability": PROBABILITY_DIR,
    }

    output_dir = output_dirs[panel_type]

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    # -----------------------------------------
    # Archivo
    # -----------------------------------------

    outfile = os.path.join(
        output_dir,
        (f"{panel_type}" f"_h{timestep:03d}.png"),
    )

    # -----------------------------------------
    # Guardar
    # -----------------------------------------

    fig.savefig(
        outfile,
        dpi=DPI,
        bbox_inches="tight",
    )

    plt.close(fig)

    return outfile


# =====================================================
# PANEL WRAPPERS
# =====================================================


def create_operational_panel(
    products,
    lon,
    lat,
    timestep,
):
    """
    Genera el panel operacional.
    """

    return create_panel(
        products=products,
        lon=lon,
        lat=lat,
        timestep=timestep,
        panel_type="operational",
    )


def create_uncertainty_panel(
    products,
    lon,
    lat,
    timestep,
):
    """
    Genera el panel de incertidumbre.
    """

    return create_panel(
        products=products,
        lon=lon,
        lat=lat,
        timestep=timestep,
        panel_type="uncertainty",
    )


def create_probability_panel(
    products,
    lon,
    lat,
    timestep,
):
    """
    Genera el panel probabilístico.
    """

    return create_panel(
        products=products,
        lon=lon,
        lat=lat,
        timestep=timestep,
        panel_type="probability",
    )


# =====================================================
# ALL PANELS
# =====================================================


def create_all_panels(
    products,
    lon,
    lat,
    timestep,
):
    """
    Genera todos los paneles para
    un timestep.

    Returns
    -------
    dict
    """

    files = {}

    files["operational"] = create_operational_panel(
        products,
        lon,
        lat,
        timestep,
    )

    files["uncertainty"] = create_uncertainty_panel(
        products,
        lon,
        lat,
        timestep,
    )

    files["probability"] = create_probability_panel(
        products,
        lon,
        lat,
        timestep,
    )

    return files
