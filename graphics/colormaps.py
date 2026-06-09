#!/usr/bin/env python3

from matplotlib.colors import (
    ListedColormap,
    BoundaryNorm,
)

from config.config import (
    RAIN_LEVELS,
    RAIN_COLORS,
    PROB_LEVELS,
    PROB_COLORS,
    SPREAD_LEVELS,
    SPREAD_COLORS,
    RELATIVE_SPREAD_LEVELS,
    RELATIVE_SPREAD_COLORS,
)

# =====================================================
# COLORMAPS
# =====================================================

RAIN_CMAP = ListedColormap(RAIN_COLORS)

RAIN_NORM = BoundaryNorm(
    RAIN_LEVELS,
    len(RAIN_COLORS),
)

PROB_CMAP = ListedColormap(PROB_COLORS)

PROB_NORM = BoundaryNorm(
    PROB_LEVELS,
    len(PROB_COLORS),
)

SPREAD_CMAP = ListedColormap(SPREAD_COLORS)

SPREAD_NORM = BoundaryNorm(
    SPREAD_LEVELS,
    len(SPREAD_COLORS),
)

RELATIVE_SPREAD_CMAP = ListedColormap(RELATIVE_SPREAD_COLORS)

RELATIVE_SPREAD_NORM = BoundaryNorm(
    RELATIVE_SPREAD_LEVELS,
    len(RELATIVE_SPREAD_COLORS),
)


# =====================================================
# STYLES
# =====================================================

STYLES = {
    "rain": (
        RAIN_CMAP,
        RAIN_NORM,
    ),
    "prob": (
        PROB_CMAP,
        PROB_NORM,
    ),
    "spread": (
        SPREAD_CMAP,
        SPREAD_NORM,
    ),
    "relative_spread": (
        RELATIVE_SPREAD_CMAP,
        RELATIVE_SPREAD_NORM,
    ),
}


# =====================================================
# API
# =====================================================


def get_style(name):
    """
    Devuelve cmap y norm.

    Parameters
    ----------
    name : str

    Returns
    -------
    tuple
        (cmap, norm)
    """

    if name not in STYLES:

        raise KeyError(f"Style '{name}' no definido")

    return STYLES[name]
