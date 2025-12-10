""" """

import numpy as np
from scipy.optimize import root, curve_fit
import matplotlib.pyplot as plt


def fvd_to_tau(fvd):
    """
    Converts a free-volume distribution (given in DIAMETER) to corresponding
    PALS lifetime (given in NANOSECONDS) using the Tau-Eldrup model
    """
    fvd = np.array(fvd)
    x = fvd / 2
    tau = (
        2 * (1 - x / (x + 1.66) + 1 / (2 * np.pi) * np.sin(2 * np.pi * x / (x + 1.66)))
    ) ** (-1)

    return tau


def tau_to_fvd(tau):
    """
    Converts a PALS lifetime distribution (given in NANOSECONDS) to corresponding
    free-volume distribution (given in DIAMETER) using the Tau-Eldrup model
    """
    fvd = np.zeros(len(tau))

    def te(x, tau):
        return 1 / tau - 2 * (
            1 - x / (x + 1.66) + 1 / (2 * np.pi) * np.sin(2 * np.pi * x / (x + 1.66))
        )

    for i, tau_val in enumerate(tau):
        result = root(te, tau_val, args=(tau_val))
        fvd[i] = result.x[0]

    return fvd * 2
