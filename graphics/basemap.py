#!/usr/bin/env python3

import os

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader

from config.config import (
    EXTENT,
    COUNTRIES_SHP,
    DEPARTMENTS_SHP,
    COASTLINE_SHP,
)

# =====================================================
# CACHE
# =====================================================

_SHAPE_CACHE = {}

_SHAPEFILES_VALIDATED = False


# =====================================================
# VALIDATION
# =====================================================


def validate_shapefiles():
    """
    Verifica que todos los shapefiles
    requeridos existan.

    La validación se ejecuta una sola vez.
    """

    global _SHAPEFILES_VALIDATED

    if _SHAPEFILES_VALIDATED:
        return

    for shp in (
        COUNTRIES_SHP,
        DEPARTMENTS_SHP,
        COASTLINE_SHP,
    ):

        if not os.path.exists(shp):

            raise FileNotFoundError(f"No existe shapefile: {shp}")

    _SHAPEFILES_VALIDATED = True


# =====================================================
# GEOMETRIES
# =====================================================


def load_geometries(shapefile):
    """
    Carga geometrías y las almacena
    en caché.

    Parameters
    ----------
    shapefile : str

    Returns
    -------
    list
    """

    validate_shapefiles()

    if shapefile not in _SHAPE_CACHE:

        reader = shpreader.Reader(shapefile)

        _SHAPE_CACHE[shapefile] = list(reader.geometries())

    return _SHAPE_CACHE[shapefile]


# =====================================================
# GENERIC SHAPEFILE DRAWER
# =====================================================


def add_shapefile(
    ax,
    shapefile,
    edgecolor="black",
    linewidth=1.0,
    facecolor="none",
    alpha=1.0,
    zorder=10,
):
    """
    Agrega un shapefile al mapa.

    Parameters
    ----------
    ax : cartopy GeoAxes

    shapefile : str

    edgecolor : str

    linewidth : float

    facecolor : str

    alpha : float

    zorder : int
    """

    geometries = load_geometries(shapefile)

    ax.add_geometries(
        geometries,
        crs=ccrs.PlateCarree(),
        edgecolor=edgecolor,
        facecolor=facecolor,
        linewidth=linewidth,
        alpha=alpha,
        zorder=zorder,
    )


# =====================================================
# MAP LAYERS
# =====================================================


def draw_countries(ax):
    """
    Países vecinos.
    """

    add_shapefile(
        ax,
        COUNTRIES_SHP,
        edgecolor="black",
        linewidth=0.8,
        facecolor="none",
        alpha=1.0,
        zorder=20,
    )


def draw_coastline(ax):
    """
    Línea de costa de alta resolución.
    """

    add_shapefile(
        ax,
        COASTLINE_SHP,
        edgecolor="black",
        linewidth=1.2,
        facecolor="none",
        alpha=1.0,
        zorder=30,
    )


def draw_departments(ax):
    """
    División departamental.
    """

    add_shapefile(
        ax,
        DEPARTMENTS_SHP,
        edgecolor="gray",
        linewidth=0.4,
        facecolor="none",
        alpha=0.7,
        zorder=40,
    )


# =====================================================
# OVERLAYS
# =====================================================


def draw_overlays(ax):
    """
    Capas adicionales.

    Reservado para futuras expansiones.
    """

    pass


# =====================================================
# GRID
# =====================================================


def draw_grid(ax):
    """
    Grid geográfico.
    """

    import matplotlib.ticker as mticker
    from cartopy.mpl.gridliner import (
        LONGITUDE_FORMATTER,
        LATITUDE_FORMATTER,
    )

    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.3,
        linestyle="--",
        alpha=0.4,
    )

    gl.top_labels = False
    gl.right_labels = False

    gl.xlabel_style = {
        "size": 12,
    }

    gl.ylabel_style = {
        "size": 12,
    }

    gl.xformatter = mticker.FormatStrFormatter("%.1f°")

    gl.yformatter = mticker.FormatStrFormatter("%.1f°")
    return gl


# =====================================================
# BASEMAP
# =====================================================


def draw_base(
    ax,
    extent=EXTENT,
):
    """
    Dibuja el mapa base completo.

    Parameters
    ----------
    ax : cartopy GeoAxes

    extent : tuple
        (west, east, south, north)
    """

    ax.set_extent(
        extent,
        crs=ccrs.PlateCarree(),
    )

    draw_grid(ax)

    draw_countries(ax)

    draw_coastline(ax)

    draw_departments(ax)

    draw_overlays(ax)
