"""
parameters.py
-------------
Electrophysiological parameter database for Canonical Neuronal Firing Pattern Library.
Contains standard AdEx parameters for Cerebellar Granule Cell (GrC) and other cerebellar neurons.

Standard AdEx Units:
- C      : Membrane capacitance (pF)
- gL     : Leak conductance (nS)
- EL     : Reversal potential / Leak potential (mV)
- Delta_T: Exponential slope factor (mV)
- VT     : Spike-initiation threshold parameter (mV)
- tau_w  : Adaptation time constant (ms)
- I      : Applied current (pA)
- a      : Subthreshold adaptation coupling (nS)
- b      : Spike-triggered adaptation increment (pA)

Missing Spike-Reset Parameters (To be verified with PI / Literature):
- V_peak : Spike peak cutoff potential (mV) [Default baseline: 0.0 mV]
- V_reset: Spike reset potential (mV) [Default baseline: -60.0 mV]
"""

# Parameter dictionary for cerebellar neuron types
NEURON_DATABASE = {
    "GrC - Cerebellar Granule Cell": {
        "name": "Cerebellar Granule Cell (GrC)",
        "C": 1.0,         # pF
        "gL": 10.0,       # nS
        "EL": -70.0,      # mV
        "Delta_T": 2.0,   # mV
        "VT": -50.0,      # mV
        "tau_w": 0.71,    # ms
        "I": 20.0,        # pA
        "a": -10.0,       # nS
        "b": 265.0,       # pA
        "V_peak": 0.0,    # mV
        "V_reset": -60.0, # mV
        "description": "Small intrinsic excitatory granule cell of the cerebellar cortex."
    },
    "GoC - Golgi Cell": {
        "name": "Golgi Cell (GoC)",
        "C": 511.0,       # pF
        "gL": 13.1,       # nS
        "EL": -58.0,      # mV
        "Delta_T": 7.0,   # mV
        "VT": -60.0,      # mV
        "tau_w": 14.65,   # ms
        "I": 0.0,         # pA
        "a": -20.0,       # nS
        "b": 1033.0,      # pA
        "V_peak": 0.0,    # mV
        "V_reset": -50.0, # mV (Adjusted reset voltage for stable electrophysiological integration)
        "description": "Inhibitory interneuron of the cerebellar granular layer."
    },
    "PC - Purkinje Cell": {
        "name": "Purkinje Cell (PC)",
        "C": 100.0,       # pF
        "gL": 10.0,       # nS
        "EL": -65.0,      # mV
        "Delta_T": 2.0,   # mV
        "VT": -50.0,      # mV
        "tau_w": 1.0,     # ms
        "I": 0.0,         # pA
        "a": -13.0,       # nS
        "b": 260.0,       # pA
        "V_peak": 0.0,    # mV
        "V_reset": -60.0, # mV
        "description": "Principal inhibitory output neuron of the cerebellar cortex."
    },
    "IO - Inferior Olive Cell": {
        "name": "Inferior Olive Cell (IO)",
        "C": 350.0,       # pF
        "gL": 10.0,       # nS
        "EL": -65.0,      # mV
        "Delta_T": 2.0,   # mV
        "VT": -50.0,      # mV
        "tau_w": 1.0,     # ms
        "I": 0.0,         # pA
        "a": -13.0,       # nS
        "b": 1200.0,      # pA
        "V_peak": 0.0,    # mV
        "V_reset": -60.0, # mV
        "description": "Climbing fiber source projection neuron in inferior olive."
    },
    "DCN - Deep Cerebellar Nuclei": {
        "name": "Deep Cerebellar Nuclei (DCN)",
        "C": 200.0,       # pF
        "gL": 10.0,       # nS
        "EL": -70.0,      # mV
        "Delta_T": 2.0,   # mV
        "VT": -50.0,      # mV
        "tau_w": 8.0,     # ms
        "I": 0.0,         # pA
        "a": -20.0,       # nS
        "b": 675.0,       # pA
        "V_peak": 0.0,    # mV
        "V_reset": -60.0, # mV
        "description": "Primary output neurons of the cerebellum."
    }
}

PARAM_METADATA = {
    "C": {"unit": "pF", "name": "Membrane Capacitance"},
    "gL": {"unit": "nS", "name": "Leak Conductance"},
    "EL": {"unit": "mV", "name": "Leak Potential / Reversal Potential"},
    "Delta_T": {"unit": "mV", "name": "Slope Factor"},
    "VT": {"unit": "mV", "name": "Spike-Initiation Threshold"},
    "tau_w": {"unit": "ms", "name": "Adaptation Time Constant"},
    "I": {"unit": "pA", "name": "Applied / Injected Current"},
    "a": {"unit": "nS", "name": "Subthreshold Adaptation Coupling"},
    "b": {"unit": "pA", "name": "Spike-Triggered Adaptation Increment"},
    "V_peak": {"unit": "mV", "name": "Spike Peak Threshold"},
    "V_reset": {"unit": "mV", "name": "Post-Spike Reset Voltage"}
}


def get_neuron_params(neuron_key: str) -> dict:
    """Retrieve parameter dictionary for a given neuron key."""
    if neuron_key not in NEURON_DATABASE:
        raise KeyError(f"Neuron '{neuron_key}' not found in database.")
    return NEURON_DATABASE[neuron_key].copy()


def list_available_neurons() -> list:
    """Return a list of available neuron keys."""
    return list(NEURON_DATABASE.keys())

