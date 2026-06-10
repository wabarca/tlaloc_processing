import numpy as np


def accumulate_period(
    ensemble,
    start,
    end,
):
    """
    ensemble:
        (time,members,y,x)

    return:
        (members,y,x)
    """

    return np.sum(
        ensemble[start:end],
        axis=0,
        dtype=np.float32,
    )


def rolling_windows(nt, hours):
    windows = []

    for start in range(0, nt, hours):

        end = min(start + hours, nt)

        windows.append((start, end))

    return windows
