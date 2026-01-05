"""
timephase_utils.py

Utilities for simulating GW signals in noise and analysing
time / phase / SNR uncertainties.
"""

from typing import Dict, List, Tuple

import numpy as np
import pycbc.noise
import pycbc.psd
import pycbc.waveform
import pycbc.filter
from pycbc.types import FrequencySeries
from sklearn.linear_model import LinearRegression


# ============================================================================
# Simulation & injection utilities
# ============================================================================

def psd(duration: float = 4.0,
        flow: float = 20.0,
        sample_rate: float = 8192.0) -> FrequencySeries:
    """
    Construct a (aLIGOZeroDetHighPower) PSD for a given segment duration.

    Parameters
    ----------
    duration : float
        Length of the data segment in seconds.
    flow : float, optional
        Low-frequency cutoff for the PSD.
    sample_rate : float, optional
        Sampling rate in Hz (default 4096).

    Returns
    -------
    pycbc.types.FrequencySeries
        The generated PSD.
    """
    delta_f = 1.0 / duration
    flen = int(sample_rate / delta_f) + 1
    return pycbc.psd.aLIGOZeroDetHighPower(flen, delta_f, flow)


def noise(duration: float,
          input_psd: FrequencySeries,
          sample_rate: float = 8192.0):
    """
    Generate a noise realisation from a PSD and return its frequency series.

    Parameters
    ----------
    duration : float
        Length of the data segment in seconds.
    input_psd : FrequencySeries
        PSD to draw noise from.
    sample_rate : float, optional
        Sampling rate in Hz (default 4096).

    Returns
    -------
    pycbc.types.FrequencySeries
        The noise realisation in the frequency domain.
    """
    # This mirrors your original delta_t expression
    delta_t = 1.0 / sample_rate
    tsamples = int(duration / delta_t)
    ts = pycbc.noise.noise_from_psd(tsamples, delta_t, input_psd)
    return ts.to_frequencyseries()


def waveform(stilde,
             m1: float,
             m2: float,
             dist: float,
             approximant: str = "IMRPhenomD",
             f_lower: float = 20.0):
    """
    Generate an FD waveform and resize it to match `stilde`.

    Parameters
    ----------
    stilde : FrequencySeries
        Frequency-domain data whose length / delta_f we match.
    m1, m2 : float
        Component masses (solar masses).
    dist : float
        Luminosity distance (Mpc).
    approximant : str, optional
        Waveform approximant to use.
    f_lower : float, optional
        Low-frequency cutoff.

    Returns
    -------
    pycbc.types.FrequencySeries
        The + polarisation frequency-domain waveform (hp).
    """
    hp, hc = pycbc.waveform.get_fd_waveform(
        approximant=approximant,
        mass1=m1,
        mass2=m2,
        f_lower=f_lower,
        delta_f=stilde.delta_f,
        distance=dist,
    )
    hp.resize(len(stilde))
    return hp


def combine(stilde,
            hp,
            input_time: float,
            duration: float):
    """
    Inject a time-shifted waveform into the noise realisation.

    Parameters
    ----------
    stilde : FrequencySeries
        Noise (FD) data.
    hp : FrequencySeries
        Signal waveform (FD).
    input_time : float
        Injection time (same units as snr.sample_times).
    duration : float
        Segment duration.

    Returns
    -------
    pycbc.types.FrequencySeries
        Data = noise + injected signal.
    """
    time_shift = input_time % duration
    hp_shifted = hp.cyclic_time_shift(time_shift)
    return stilde + hp_shifted


def unc(hp,
        data,
        input_psd: FrequencySeries,
        input_time: float,
        f_low: float = 20.0):
    """
    Compute time / phase / SNR uncertainties for one injection.

    Parameters
    ----------
    hp : FrequencySeries
        Template waveform used for matched filtering.
    data : FrequencySeries
        Data (noise + signal) to filter.
    input_psd : FrequencySeries
        PSD used in matched filtering.
    input_time : float
        True injection time.
    f_low : float, optional
        Low-frequency cutoff for matched filter and sigmasq.

    Returns
    -------
    tuple
        (input_snr, dt, dp, ds) where
        dt = input_time - recovered_time,
        dp = input_phase - recovered_phase (wrapped to [-pi, pi]),
        ds = input_snr - recovered_snr.
    """
    snr = pycbc.filter.matched_filter(
        hp,
        data,
        psd=input_psd,
        low_frequency_cutoff=f_low,
    )

    snr_np = snr.numpy()
    hp_np = hp.numpy()

    snr_peak = snr[np.argmax(np.abs(snr_np))]
    hp_peak = hp[np.argmax(np.abs(hp_np))]

    input_phase = np.arctan2(np.imag(hp_peak), np.real(hp_peak))

    snr_sq = pycbc.filter.sigmasq(hp, psd=input_psd, low_frequency_cutoff=f_low)
    input_snr = np.sqrt(snr_sq)

    output_time = snr.sample_times[np.argmax(np.abs(snr_np))]
    output_phase = np.arctan2(np.imag(snr_peak), np.real(snr_peak))

    dt = input_time - output_time
    output_snr = np.abs(snr_peak)
    ds = input_snr - output_snr

    dp = input_phase - output_phase
    if dp > np.pi:
        dp -= 2 * np.pi
    elif dp < -np.pi:
        dp += 2 * np.pi

    return input_snr, dt, dp, ds


def datacuts(t_data: np.ndarray,
             p_data: np.ndarray,
             s_data: np.ndarray,
             snr_data: np.ndarray):
    """
    Apply your empirical data cuts in (t, p) space.

    Parameters
    ----------
    t_data, p_data, s_data : np.ndarray
        Arrays of time, phase and SNR-like quantity.

    Returns
    -------
    tuple of np.ndarray
        (t_filtered, p_filtered, s_filtered)
    """
    mask = (t_data < -0.002) & (p_data > 1.5)
    t2 = t_data[~mask]
    p2 = p_data[~mask]
    s2 = s_data[~mask]
    snr2 = snr_data[~mask]

    mask2 = (t2 > 0.002) & (p2 < -1.5)
    t3 = t2[~mask2]
    p3 = p2[~mask2]
    s3 = s2[~mask2]
    snr3 = snr2[~mask2]

    return t3, p3, s3, snr3


# ============================================================================
# Result aggregation utilities
# ============================================================================

def compute_results_for_sets(
    noise_list: List[FrequencySeries],
    wf_dict: Dict[str, FrequencySeries],
    input_time: float,
    duration: float,
    t_unc_cut: float = 0.01,
) -> Dict[str, List[Dict[str, float]]]:
    """
    Compute SNR, time and phase uncertainties for all waveforms across
    all noise realisations.

    Parameters
    ----------
    noise_list : list of FrequencySeries
        List of noise frequency series.
    wf_dict : dict
        Mapping name -> waveform frequency series.
    input_time : float
        Injection time.
    duration : float
        Segment duration.
    t_unc_cut : float, optional
        Cut on |t_unc|; events outside this are discarded.

    Returns
    -------
    dict
        name -> list of dicts with keys 'snr', 't_unc', 'p_unc', 's_unc'.
    """
    results: Dict[str, List[Dict[str, float]]] = {name: [] for name in wf_dict}
    base_psd = psd(duration)

    for n in noise_list:
        for name, wf in wf_dict.items():
            waveform_fd = wf.copy()
            data = combine(n, wf, input_time, duration)
            snr_val, t_unc, p_unc, s_unc = unc(waveform_fd, data, base_psd, input_time)

            if np.abs(t_unc) > t_unc_cut:
                continue

            results[name].append(
                {
                    "snr": float(snr_val),
                    "t_unc": float(t_unc),
                    "p_unc": float(p_unc),
                    "s_unc": float(s_unc),
                }
            )
    return results


def sorted_arrays_from_results(
    results: Dict[str, List[Dict[str, float]]]
) -> Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    """
    Convert results dict from compute_results_for_sets into arrays.

    Parameters
    ----------
    results : dict
        name -> list of dicts with keys 'snr', 't_unc', 'p_unc', 's_unc'.

    Returns
    -------
    dict
        name -> (t_unc_array, p_unc_array, snr_array, s_unc_array).
    """
    out: Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}

    for name, lst in results.items():
        t = np.array([r["t_unc"] for r in lst])
        p = np.array([r["p_unc"] for r in lst])
        s = np.array([r["s_unc"] for r in lst])
        snr = np.array([r["snr"] for r in lst])
        out[name] = (t, p, s, snr)

    return out


# ============================================================================
# Fitting utilities
# ============================================================================

def fit_polynomial_t_vs_p(
    all_p: np.ndarray,
    all_t: np.ndarray,
    deg: int = 3,
):
    """
    Fit a polynomial model t(p).

    Parameters
    ----------
    all_p : array-like
        Phase uncertainties.
    all_t : array-like
        Time uncertainties.
    deg : int, optional
        Polynomial degree.

    Returns
    -------
    coefs : np.ndarray
        Polynomial coefficients (highest power first).
    model : np.poly1d
        Callable polynomial model.
    """
    coefs = np.polyfit(all_p, all_t, deg)
    model = np.poly1d(coefs)
    return coefs, model


def fit_std_vs_inv_snr(
    stds: np.ndarray,
    snrs: np.ndarray,
    fit_intercept: bool = False,
):
    """
    Fit a linear model std = k * (1/SNR) [+ intercept],
    and estimate the uncertainty on k.

    Parameters
    ----------
    stds : array-like
        Measured standard deviations (response).
    snrs : array-like
        SNR values corresponding to each std.
    fit_intercept : bool, optional
        Whether to fit an intercept term.

    Returns
    -------
    intercept : float or np.ndarray
        Fitted intercept.
    k : float
        Fitted slope.
    se_k : float
        Standard error (uncertainty) on k.
    lr : sklearn.linear_model.LinearRegression
        Fitted model instance.
    """
    Z = (1.0 / np.array(snrs)).reshape(-1, 1)  # predictor = 1/SNR
    x = np.array(stds).reshape(-1, 1)          # response variable

    lr = LinearRegression(fit_intercept=fit_intercept).fit(Z, x)

    k = lr.coef_[0][0]
    intercept = lr.intercept_

    # Residuals
    y_pred = lr.predict(Z)
    residuals = x - y_pred

    N = len(Z)
    n_params = 2 if fit_intercept else 1  # slope + optional intercept
    dof = N - n_params

    # residual variance estimate
    sigma2 = np.sum(residuals**2) / dof

    # variance and standard error of k
    var_k = sigma2 / np.sum(Z**2)
    se_k = float(np.sqrt(var_k))

    return intercept, float(k), se_k, lr


def apply_datacuts_to_dict(
    dict_of_arrays: Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]
) -> Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]:
    """
    Apply datacuts() to all named arrays in a dict.

    Parameters
    ----------
    dict_of_arrays : dict
        name -> (t, p, s, ds)

    Returns
    -------
    dict
        name -> (t_cut, p_cut, s_cut, ds)  # ds unchanged here; adjust if desired.
    """
    out: Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = {}

    for name, (t, p, s, snr) in dict_of_arrays.items():
        t2, p2, s2, snr2 = datacuts(t, p, s, snr)
        # If you also want ds cut consistently, you can change this to:
        # mask = np.isin(t, t2)  # or build mask explicitly
        out[name] = (t2, p2, s2, snr2)

    return out