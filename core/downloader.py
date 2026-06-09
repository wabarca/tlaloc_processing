#!/usr/bin/env python3

import os
import threading

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

import requests

from requests.adapters import HTTPAdapter

from urllib3.util.retry import Retry

from tqdm import tqdm

from config.config import (
    BASE_URL,
    RAW_DIR,
    DOWNLOAD_WORKERS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_BACKOFF,
    MEMBERS,
    NT,
)

_thread_local = threading.local()


def create_session():
    """
    Crea una sesión HTTP con pool de conexiones y reintentos.
    """

    retry = Retry(
        total=MAX_RETRIES,
        connect=MAX_RETRIES,
        read=MAX_RETRIES,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=[
            429,
            500,
            502,
            503,
            504,
        ],
        allowed_methods={"GET"},
    )

    adapter = HTTPAdapter(
        pool_connections=DOWNLOAD_WORKERS,
        pool_maxsize=DOWNLOAD_WORKERS,
        max_retries=retry,
    )

    session = requests.Session()

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def get_session():
    """
    Una sesión persistente por hilo.
    """

    if not hasattr(_thread_local, "session"):
        _thread_local.session = create_session()

    return _thread_local.session


def download(session, member, timestep):
    """
    Descarga un GeoTIFF individual.
    """

    url = f"{BASE_URL}/{member}/dominio2/00/" f"geotiff/lluvia_{timestep}.tif"

    outfile = f"{RAW_DIR}/" f"{member}_{timestep}.tif"

    if os.path.exists(outfile) and os.path.getsize(outfile) > 1000:
        return outfile

    response = session.get(
        url,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    if len(response.content) < 1000:
        raise RuntimeError(f"Archivo sospechoso: {url}")

    tmpfile = outfile + ".tmp"

    with open(tmpfile, "wb") as f:
        f.write(response.content)

    os.replace(tmpfile, outfile)

    return outfile


def download_worker(task):
    """
    Worker para ThreadPoolExecutor.
    """

    member, timestep = task

    session = get_session()

    return download(
        session,
        member,
        timestep,
    )


def download_all():
    """
    Descarga todos los miembros y tiempos.
    """

    os.makedirs(
        RAW_DIR,
        exist_ok=True,
    )

    tasks = [(member, timestep) for member in MEMBERS for timestep in range(1, NT + 1)]

    total = len(tasks)

    print(f"Descargando {total} archivos " f"con {DOWNLOAD_WORKERS} workers")

    with ThreadPoolExecutor(max_workers=DOWNLOAD_WORKERS) as executor:

        futures = [
            executor.submit(
                download_worker,
                task,
            )
            for task in tasks
        ]

        for future in tqdm(
            as_completed(futures),
            total=total,
            desc="Descargando",
        ):
            future.result()

    print("Descarga completada")
