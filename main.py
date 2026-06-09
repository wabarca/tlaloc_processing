#!/usr/bin/env python3

import time

from tqdm import tqdm

from core.downloader import download_all
from core.reader import load_ensemble
from core.ensemble import compute_products

from graphics.panels import (
    create_all_panels,
)

from config.config import NT

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
        range(NT),
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
