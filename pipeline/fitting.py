import numpy as np
from scipy.optimize import leastsq


def double_lognormal(x, params):
    """Sum of two log-normal-like peaks:

    Args:
        x: independent variable
        params: log-normal fit parameters (c1, mu1, sigma1, c2, mu2, sigma2)
    """
    c1, mu1, sigma1, c2, mu2, sigma2 = params

    ln_x = np.log(x)
    y = c1 / x * np.exp(-((ln_x - mu1) ** 2) / (2 * sigma1**2)) + c2 / x * np.exp(
        -((ln_x - mu2) ** 2) / (2 * sigma2**2)
    )

    return y


def single_lognormal(x, params):
    """Single log-normal-like peak

    Args:
        x: independent variable
        params: log-normal fit parameters (c, mu, sigma)
    """
    c1, mu1, sigma1 = params

    ln_x = np.log(x)
    y = c1 / x * np.exp(-((ln_x - mu1) ** 2) / (2 * sigma1**2))

    return y


def n_lognormal(x, params):
    """Sum of n log-normal-like peaks

    Args:
        x: independent variable
        params: log-normal fit parameters (c1, mu1, sigma1, c2, mu2, sigma2, ...)
    """

    ln_x = np.log(x)

    n_peaks = len(params) // 3

    for i in range(n_peaks):
        c = params[3 * i]
        mu = params[3 * i + 1]
        sigma = params[3 * i + 2]

        y += c / x * np.exp(-((ln_x - mu) ** 2) / (2 * sigma**2))

    return y


def perform_fit(c1, mu1, sigma1, c2, mu2, sigma2, x, y):
    """
    Fit double log-normal.
    """

    def fit(params, x, y):
        return double_lognormal(x, params) - y

    p0 = [c1, mu1, sigma1, c2, mu2, sigma2]
    fit = leastsq(fit, p0, args=(x, y))

    return fit[0]


def convert_timescale(params_opt, timescale):
    """Convert bimodal log-normal fit parameters by some timescale factor

    Justification: c absorbs the 1/t from the log-normal definition -> scales linearly with timescale
    mu is in log-space -> shifts by log(timescale)
    sigma is dimensionless -> does not change
    """

    return [
        timescale * params_opt[0],
        params_opt[1] + np.log(timescale),
        params_opt[2],
        timescale * params_opt[3],
        params_opt[4] + np.log(timescale),
        params_opt[5],
    ]


def area_under_lognormal(c, sigma):
    return c * sigma * np.sqrt(2 * np.pi)


def c_from_area(area, sigma):
    return area / (sigma * np.sqrt(2 * np.pi))
