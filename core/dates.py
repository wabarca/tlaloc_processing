#!/usr/bin/env python3

from datetime import (
    datetime,
    timedelta,
)

# =====================================================
# RUN
# =====================================================


def get_run_datetime():
    """
    Fecha y hora UTC actuales.

    Returns
    -------
    datetime
    """

    return datetime.utcnow()


def get_run_date():
    """
    Fecha UTC del ciclo.

    Returns
    -------
    date
    """

    return get_run_datetime().date()


# =====================================================
# VALID TIMES
# =====================================================


def get_start_valid_time():
    """
    Tiempo válido asociado al primer
    GeoTIFF disponible.

    Convención actual Tlaloc:

        GeoTIFF 1 = 00 UTC del día anterior

    Returns
    -------
    datetime
    """

    run_date = get_run_date()

    return datetime.combine(
        run_date,
        datetime.min.time(),
    ) - timedelta(days=1)


def get_valid_time(timestep):
    """
    Devuelve la fecha válida asociada
    a un timestep.

    Parameters
    ----------
    timestep : int
        1..NT

    Returns
    -------
    datetime
    """

    return get_start_valid_time() + timedelta(hours=timestep - 1)


def format_valid_time(
    timestep,
    fmt="%Y-%m-%d %H:%M UTC",
):
    """
    Devuelve fecha válida formateada.

    Parameters
    ----------
    timestep : int

    fmt : str

    Returns
    -------
    str
    """

    return get_valid_time(timestep).strftime(fmt)


# =====================================================
# FORECAST WINDOWS
# =====================================================


def get_window_times(
    start_timestep,
    end_timestep,
):
    """
    Devuelve inicio y fin de una ventana.

    Ejemplo:
        1-6h
        7-12h
        19-42h

    Returns
    -------
    tuple(datetime, datetime)
    """

    start_time = get_valid_time(start_timestep)

    end_time = get_valid_time(end_timestep)

    return (
        start_time,
        end_time,
    )


def format_window(
    start_timestep,
    end_timestep,
):
    """
    Texto legible para paneles.

    Example:
        2026-08-10 00 UTC
        -
        2026-08-10 05 UTC
    """

    start_time, end_time = get_window_times(
        start_timestep,
        end_timestep,
    )

    return f"{start_time:%Y-%m-%d %H:%M UTC}" f" - " f"{end_time:%Y-%m-%d %H:%M UTC}"


# =====================================================
# FORECAST DAY
# =====================================================


def forecast_day(timestep):
    """
    Día de pronóstico relativo.

    Returns
    -------
    int

    Examples
    --------
    timestep 1  -> Day 0
    timestep 25 -> Day 1
    timestep 49 -> Day 2
    """

    return (timestep - 1) // 24


def forecast_hour(timestep):
    """
    Hora relativa desde el inicio.

    Returns
    -------
    int
    """

    return timestep - 1
