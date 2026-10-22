"""
analysis.py
-----------
Spike detection and electrophysiological firing-pattern metrics calculation module.

Metrics calculated:
- Total Spike Count
- Mean Firing Frequency (Hz)
- Inter-Spike Intervals (ISI, ms)
- Mean ISI (ms) and Standard Deviation of ISI (ms)
- Coefficient of Variation of ISI (CV = std_isi / mean_isi)
- Qualitative Firing Classification (Quiescent, Single Spike, Tonic, Bursting/Irregular)
"""

import numpy as np


def analyze_firing_pattern(spike_times: np.ndarray, duration_ms: float) -> dict:
    """
    Calculate electrophysiological firing metrics from spike time series.

    Parameters:
    -----------
    spike_times : np.ndarray or list
        List or array of detected spike timestamps (in ms).
    duration_ms : float
        Total duration of simulation (in ms).

    Returns:
    --------
    dict containing calculated metrics.
    """
    spike_times = np.array(spike_times)
    num_spikes = len(spike_times)
    duration_sec = duration_ms / 1000.0

    # Overall mean firing rate over total simulation time
    mean_frequency_hz = num_spikes / duration_sec if duration_sec > 0 else 0.0

    if num_spikes < 2:
        return {
            "num_spikes": num_spikes,
            "mean_frequency_hz": mean_frequency_hz,
            "isi_ms": [],
            "mean_isi_ms": None,
            "std_isi_ms": None,
            "cv_isi": None,
            "firing_mode": "Quiescent / Subthreshold" if num_spikes == 0 else "Single Spike Response",
            "message": "Insufficient spikes (< 2) to compute Inter-Spike Interval (ISI) metrics."
        }

    # Inter-Spike Intervals (ISI) in milliseconds
    isi_ms = np.diff(spike_times)
    mean_isi = float(np.mean(isi_ms))
    std_isi = float(np.std(isi_ms, ddof=1)) if len(isi_ms) > 1 else 0.0

    # Coefficient of Variation of ISI (CV = std / mean)
    cv_isi = std_isi / mean_isi if mean_isi > 0 else 0.0

    # Classification of firing pattern
    if cv_isi < 0.1:
        firing_mode = "Tonic / Regular Spiking"
    elif cv_isi < 0.5:
        firing_mode = "Adaptative / Slightly Irregular Spiking"
    else:
        firing_mode = "Bursting / Highly Irregular Spiking"

    return {
        "num_spikes": num_spikes,
        "mean_frequency_hz": round(mean_frequency_hz, 2),
        "isi_ms": np.round(isi_ms, 3).tolist(),
        "mean_isi_ms": round(mean_isi, 3),
        "std_isi_ms": round(std_isi, 3),
        "cv_isi": round(cv_isi, 3),
        "firing_mode": firing_mode,
        "message": f"Successfully calculated ISI metrics for {num_spikes} spikes."
    }
