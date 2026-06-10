#!/usr/bin/env python3

import os

import numpy as np
import rasterio

from tqdm import tqdm

from config.config import (
    RAW_DIR,
    MEMBERS,
    NT,
    EXTENT,
)


def read_geotiff(path):
    """
    Lee un GeoTIFF y devuelve:
        data      : ndarray
        transform : affine transform
    """

    with rasterio.open(path) as src:

        data = src.read(
            1,
            out_dtype=np.float32,
        )
        transform = src.transform

        print(path)

        print(
            np.nanmin(data),
            np.nanmax(data),
        )

    return data, transform


def build_coordinates(
    transform,
    nx,
    ny,
):
    """
    Construye mallas lon/lat
    a partir del Affine transform.

    Returns
    -------
    lon : ndarray
    lat : ndarray
    """

    cols = np.arange(nx, dtype=np.float32)

    rows = np.arange(ny, dtype=np.float32)

    x = transform.c + (cols + 0.5) * transform.a

    y = transform.f + (rows + 0.5) * transform.e

    lon, lat = np.meshgrid(
        x,
        y,
    )

    return (
        lon.astype(np.float32),
        lat.astype(np.float32),
    )


def load_ensemble():
    """
    Construye el cubo completo del ensemble.

    Dimensions
    ----------
    ensemble :
        (time, member, y, x)

    Returns
    -------
    ensemble : np.ndarray
        Shape:
        (NT, n_members, ny, nx)

    lon : np.ndarray
        Longitudes de los centros de celda.

        Shape:
        (ny, nx)

    lat : np.ndarray
        Latitudes de los centros de celda.

        Shape:
        (ny, nx)

    transform : affine.Affine
        Transformación geográfica del GeoTIFF.
    """

    print("Cargando ensemble")

    first_file = os.path.join(RAW_DIR, f"{MEMBERS[0]}_1.tif")

    if not os.path.exists(first_file):
        raise FileNotFoundError(f"No existe archivo: {first_file}")

    first_data, transform = read_geotiff(first_file)

    ny, nx = first_data.shape

    lon, lat = build_coordinates(
        transform,
        nx,
        ny,
    )

    ensemble = np.empty(
        (
            NT,
            len(MEMBERS),
            ny,
            nx,
        ),
        dtype=np.float32,
    )

    print(f"Ensemble: {NT} tiempos, " f"{len(MEMBERS)} miembros, " f"{ny}x{nx}")

    for t in tqdm(range(1, NT + 1), desc="Leyendo ensemble"):

        for member_index, member in enumerate(MEMBERS):

            path = os.path.join(RAW_DIR, f"{member}_{t}.tif")

            if not os.path.exists(path):
                raise FileNotFoundError(f"No existe archivo: {path}")

            data, _ = read_geotiff(path)

            if data.shape != (ny, nx):

                raise ValueError(
                    f"Dimensiones inconsistentes en {path}: "
                    f"{data.shape} != {(ny, nx)}"
                )

            ensemble[t - 1, member_index, :, :] = data

    return (
        ensemble,
        lon,
        lat,
        transform,
    )
