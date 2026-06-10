#!/usr/bin/env python3

import time

from tqdm import tqdm

from core.downloader import download_all
from core.reader import load_ensemble
from core.ensemble import compute_products

from graphics.panels import (
    create_all_panels,
)

from core.accumulations import (
    accumulate_period,
    rolling_windows,
)

# =====================================================
# TIMESTEP
# =====================================================


def process_timestep(
    stack,
    lon,
    lat,
    timestep,
):
    """
    Procesa un timestep completo.

    Parameters
    ----------
    stack : np.ndarray
        Shape:
        (members, y, x)

    lon : np.ndarray

    lat : np.ndarray

    timestep : int
    """

    products = compute_products(stack)

    create_all_panels(
        products=products,
        lon=lon,
        lat=lat,
        timestep=timestep,
    )


# =====================================================
# FORECAST
# =====================================================

# =====================================================
# 6 HOUR ACCUMULATIONS
# =====================================================


def process_6h_accumulations(
    ensemble,
    lon,
    lat,
):

    print("Generando acumulados 6h")

    nt = ensemble.shape[0]

    for start, end in rolling_windows(nt, 6):

        stack = accumulate_period(
            ensemble,
            start,
            end,
        )

        products = compute_products(stack)

        create_all_panels(
            products=products,
            lon=lon,
            lat=lat,
            timestep=end,
            suffix="_acc06",
        )


# =====================================================
# DAILY ACCUMULATIONS
# =====================================================


def process_daily_accumulations(
    ensemble,
    lon,
    lat,
):

    print("Generando acumulados diarios")

    periods = [
        ("day1", 0, 24),
        ("day2", 24, 48),
        ("day3", 48, 72),
    ]

    for label, start, end in periods:

        if start >= ensemble.shape[0]:
            continue

        end = min(
            end,
            ensemble.shape[0],
        )

        stack = accumulate_period(
            ensemble,
            start,
            end,
        )

        products = compute_products(stack)

        create_all_panels(
            products=products,
            lon=lon,
            lat=lat,
            timestep=end,
            suffix=f"_{label}",
        )


# =====================================================
# CUMULATIVE ACCUMULATIONS
# =====================================================


def process_cumulative_accumulations(
    ensemble,
    lon,
    lat,
):

    print("Generando acumulados 48h y 72h")

    for hours in [48, 72]:

        if hours > ensemble.shape[0]:
            continue

        stack = accumulate_period(
            ensemble,
            0,
            hours,
        )

        products = compute_products(stack)

        create_all_panels(
            products=products,
            lon=lon,
            lat=lat,
            timestep=hours,
            suffix=f"_acc{hours}",
        )


def process_forecast(
    ensemble,
    lon,
    lat,
):
    """
    Procesa todos los tiempos del ensemble.
    """

    print("Generando productos")

    for t in tqdm(
        range(ensemble.shape[0]),
        desc="Procesando",
    ):

        stack = ensemble[t]

        process_timestep(
            stack=stack,
            lon=lon,
            lat=lat,
            timestep=t + 1,
        )


# =====================================================
# MAIN
# =====================================================


def main():

    total_start = time.time()

    try:

        # -------------------------------------
        # Descarga
        # -------------------------------------

        start = time.time()

        download_all()

        print(f"Descarga: " f"{time.time() - start:.1f} s")

        # -------------------------------------
        # Lectura
        # -------------------------------------

        start = time.time()

        (
            ensemble,
            lon,
            lat,
            _,
        ) = load_ensemble()

        print(f"Lectura: " f"{time.time() - start:.1f} s")

        # -------------------------------------
        # Procesamiento
        # -------------------------------------

        start = time.time()

        process_6h_accumulations(
            ensemble,
            lon,
            lat,
        )

        process_daily_accumulations(
            ensemble,
            lon,
            lat,
        )

        process_cumulative_accumulations(
            ensemble,
            lon,
            lat,
        )

        process_forecast(
            ensemble,
            lon,
            lat,
        )

        print(f"Procesamiento: " f"{time.time() - start:.1f} s")

        # -------------------------------------
        # Total
        # -------------------------------------

        print(f"Tiempo total: " f"{time.time() - total_start:.1f} s")

        print("TLALOC finalizado correctamente")

    except Exception as e:

        print("\nERROR DURANTE LA EJECUCIÓN\n")

        raise


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()
