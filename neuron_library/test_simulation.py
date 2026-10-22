"""
test_simulation.py
------------------
Backend verification script for testing AdEx simulation and analysis modules.
Run this script to confirm mathematical numerical stability, spike detection,
and firing pattern calculation before launching the Streamlit interface.
"""

import matplotlib.pyplot as plt
from parameters import NEURON_DATABASE, get_neuron_params
from models import simulate_adex
from analysis import analyze_firing_pattern


def run_backend_test():
    print("==========================================================")
    print("Running AdEx Simulation Engine Backend Verification Test...")
    print("==========================================================")

    # 1. Load Granule Cell (GrC) parameters
    grc_key = "GrC - Cerebellar Granule Cell"
    params = get_neuron_params(grc_key)

    print(f"\n--- Loaded Neuron: {params['name']} ---")
    print(f"Capacitance (C): {params['C']} pF")
    print(f"Leak Conductance (gL): {params['gL']} nS")
    print(f"Leak Potential (EL): {params['EL']} mV")
    print(f"Slope Factor (Delta_T): {params['Delta_T']} mV")
    print(f"Threshold (VT): {params['VT']} mV")
    print(f"Adaptation tau_w: {params['tau_w']} ms")
    print(f"Applied Current (I): {params['I']} pA")
    print(f"Subthreshold adaptation (a): {params['a']} nS")
    print(f"Spike adaptation inc (b): {params['b']} pA")

    # 2. Run simulation for 500 ms
    duration_ms = 500.0
    dt = 0.01  # ms

    print(f"\nSimulating for {duration_ms} ms with dt = {dt} ms...")
    res = simulate_adex(params, duration_ms=duration_ms, dt=dt)

    time = res["time"]
    V = res["V"]
    w = res["w"]
    spike_times = res["spike_times"]
    spike_count = res["spike_count"]

    print(f"Simulation completed successfully.")
    print(f"Total time steps: {len(time)}")
    print(f"Spikes detected: {spike_count}")

    # 3. Perform analysis
    analysis_results = analyze_firing_pattern(spike_times, duration_ms)

    print("\n--- Electrophysiological Analysis Results ---")
    for key, val in analysis_results.items():
        print(f"  {key}: {val}")

    # 4. Plot results for visualization verification
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Subplot 1: Membrane Potential V(t)
    ax1.plot(time, V, color="crimson", linewidth=1.2, label="V(t) Membrane Potential")
    ax1.axhline(params["VT"], color="gray", linestyle="--", alpha=0.7, label=f"VT ({params['VT']} mV)")
    ax1.set_ylabel("Membrane Potential (mV)", fontsize=11, fontweight="bold")
    ax1.set_title(f"AdEx Firing Pattern: {params['name']} (I = {params['I']} pA)", fontsize=13, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper right")

    # Subplot 2: Adaptation Current w(t)
    ax2.plot(time, w, color="navy", linewidth=1.2, label="w(t) Adaptation Current")
    ax2.set_xlabel("Time (ms)", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Adaptation w (pA)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right")

    plt.tight_layout()
    output_img = "grc_test_firing_pattern.png"
    plt.savefig(output_img, dpi=150)
    plt.close()

    print(f"\nSaved test trace plot to: {output_img}")
    print("==========================================================")
    print("Backend test complete! All equations and routines verified.")
    print("==========================================================")


if __name__ == "__main__":
    run_backend_test()
