#!/usr/bin/env python3

import numpy as np

from config.config import (
    PROBABILITY_THRESHOLDS,
    PERCENTILES,
    MIN_RELATIVE_SPREAD_MEAN,
)

# =====================================================
# TENDENCIA CENTRAL
# =====================================================


def mean_field(stack):
    """
    Media del ensemble.
    """

    return np.mean(
        stack,
        axis=0,
        dtype=np.float32,
    )


def median_field(stack):
    """
    Mediana del ensemble.
    """

    return np.median(
        stack,
        axis=0,
    ).astype(np.float32)


# =====================================================
# EXTREMOS
# =====================================================


def minimum_field(stack):
    """
    Mínimo del ensemble.
    """

    return np.min(
        stack,
        axis=0,
    ).astype(np.float32)


def maximum_field(stack):
    """
    Máximo del ensemble.
    """

    return np.max(
        stack,
        axis=0,
    ).astype(np.float32)


# =====================================================
# INCERTIDUMBRE
# =====================================================


def spread_field(stack):
    """
    Desviación estándar del ensemble.
    """

    return np.std(
        stack,
        axis=0,
        dtype=np.float32,
    )


def relative_spread_field(
    mean,
    spread,
):
    """
    Spread relativo (%).

    Evita divisiones por valores
    cercanos a cero.
    """

    with np.errstate(
        divide="ignore",
        invalid="ignore",
    ):

        relative_spread = np.where(
            mean > MIN_RELATIVE_SPREAD_MEAN,
            (spread / mean) * 100.0,
            0.0,
        )

    return relative_spread.astype(np.float32)


def range_field(
    minimum,
    maximum,
):
    """
    Rango del ensemble.
    """

    return (maximum - minimum).astype(np.float32)


# =====================================================
# PROBABILIDADES
# =====================================================


def probability_exceedance(
    stack,
    threshold,
):
    """
    Probabilidad de excedencia (%).
    """

    return (
        np.mean(
            stack > threshold,
            axis=0,
        )
        * 100.0
    ).astype(np.float32)


# =====================================================
# PERCENTILES
# =====================================================


def percentile_field(
    stack,
    percentile,
):
    """
    Percentil del ensemble.
    """

    return np.percentile(
        stack,
        percentile,
        axis=0,
    ).astype(np.float32)


# =====================================================
# PRODUCTOS
# =====================================================


def compute_products(stack):
    """
    Calcula todos los productos
    estadísticos del ensemble.

    Parameters
    ----------
    stack : ndarray
        Shape:
        (members, y, x)

    Returns
    -------
    dict
    """

    # -----------------------------------------
    # Tendencia central
    # -----------------------------------------

    mean = mean_field(stack)

    median = median_field(stack)

    # -----------------------------------------
    # Extremos
    # -----------------------------------------

    minimum = minimum_field(stack)

    maximum = maximum_field(stack)

    # -----------------------------------------
    # Incertidumbre
    # -----------------------------------------

    spread = spread_field(stack)

    relative_spread = relative_spread_field(
        mean,
        spread,
    )

    ensemble_range = range_field(
        minimum,
        maximum,
    )

    # -----------------------------------------
    # Probabilidades
    # -----------------------------------------

    probabilities = {}

    for threshold in PROBABILITY_THRESHOLDS:

        probabilities[threshold] = probability_exceedance(
            stack,
            threshold,
        )

    # -----------------------------------------
    # Percentiles
    # -----------------------------------------

    percentiles = {}

    for percentile in PERCENTILES:

        percentiles[percentile] = percentile_field(
            stack,
            percentile,
        )

    # -----------------------------------------
    # Salida
    # -----------------------------------------

    products = {
        "n_members": stack.shape[0],
        "mean": mean,
        "median": median,
        "minimum": minimum,
        "maximum": maximum,
        "spread": spread,
        "relative_spread": relative_spread,
        "range": ensemble_range,
        "probabilities": probabilities,
        "percentiles": percentiles,
    }

    return products
