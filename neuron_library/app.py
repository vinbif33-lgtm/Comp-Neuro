"""
app.py
------
Streamlit Graphical User Interface for Computational Neuronal Firing Pattern Library.

Features:
- Neuron selection dropdown (GrC, GoC, PC, IO, DCN)
- Parameter display table with units and descriptions
- Simulation controls (Duration, Time step dt, Applied Current override)
- Interactive membrane potential V(t) & adaptation current w(t) plots
- Spike detection and firing pattern analysis metrics display
- Scientific parameter notes & configuration
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from parameters import list_available_neurons, get_neuron_params, PARAM_METADATA
from models import simulate_adex
from analysis import analyze_firing_pattern


# Set page config
st.set_page_config(
    page_title="Computational Neuronal Firing Pattern Library",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Application Header & Title
st.title("Computational Neuronal Firing Pattern Library")
st.caption("Canonical Electrophysiological Characterization using the Adaptive Exponential Integrate-and-Fire (AdEx) Model")

st.markdown("""
Welcome. This application simulates canonical electrophysiological firing patterns of cerebellar neurons.
Select a neuron population from the sidebar, inspect its physiological parameters, configure simulation settings, and click **Generate Firing Pattern** to visualize membrane dynamics.
""")

st.divider()

# Sidebar: Control Panel
st.sidebar.header("Simulation Controls")

# 1. Neuron Selection Dropdown
available_neurons = list_available_neurons()
selected_neuron_key = st.sidebar.selectbox(
    "Select Neuron Population:",
    options=available_neurons,
    index=0  # Defaults to GrC - Cerebellar Granule Cell
)

# Retrieve default parameters for chosen neuron
base_params = get_neuron_params(selected_neuron_key)

st.sidebar.subheader("Simulation Parameters")

# 2. Simulation Duration Input (ms)
duration_ms = st.sidebar.number_input(
    "Simulation Duration (ms):",
    min_value=10.0,
    max_value=5000.0,
    value=500.0,
    step=50.0,
    help="Total simulation time window in milliseconds."
)

# 3. Integration Time Step dt (ms)
dt_ms = st.sidebar.number_input(
    "Integration Time Step dt (ms):",
    min_value=0.001,
    max_value=0.5,
    value=0.01,
    step=0.005,
    format="%.3f",
    help="Time step for numerical integration (smaller values increase precision)."
)

# 4. Optional Applied Current Override (pA)
custom_I = st.sidebar.number_input(
    "Injected Current I (pA):",
    min_value=-500.0,
    max_value=2000.0,
    value=float(base_params["I"]),
    step=5.0,
    help="Custom injected depolarizing/hyperpolarizing current step."
)

# Update parameters with custom injected current
active_params = base_params.copy()
active_params["I"] = custom_I

# Spike Reset Parameters
st.sidebar.subheader("Spike Reset Parameters")

V_peak = st.sidebar.number_input(
    "Spike Peak Threshold V_peak (mV):",
    min_value=-20.0,
    max_value=60.0,
    value=float(active_params["V_peak"]),
    step=1.0,
    help="Voltage threshold at which spike peak is registered."
)

V_reset = st.sidebar.number_input(
    "Post-Spike Reset Voltage V_reset (mV):",
    min_value=-100.0,
    max_value=-30.0,
    value=float(active_params["V_reset"]),
    step=1.0,
    help="Membrane voltage to which the cell resets immediately after a spike."
)

active_params["V_peak"] = V_peak
active_params["V_reset"] = V_reset

st.sidebar.divider()
generate_btn = st.sidebar.button("Generate Firing Pattern", type="primary", use_container_width=True)

# Main Body: Layout into columns
col_left, col_right = st.columns([1.2, 0.8])

with col_left:
    st.subheader(f"Parameter Table: {active_params['name']}")
    st.write(f"**Description:** {active_params['description']}")

    # Build Pandas DataFrame for neat display
    table_data = []
    for key in ["C", "gL", "EL", "Delta_T", "VT", "tau_w", "I", "a", "b", "V_peak", "V_reset"]:
        meta = PARAM_METADATA[key]
        table_data.append({
            "Parameter Symbol": key,
            "Description": meta["name"],
            "Value": active_params[key],
            "Unit": meta["unit"]
        })

    df_params = pd.DataFrame(table_data)
    st.dataframe(df_params, use_container_width=True, hide_index=True)

with col_right:
    st.subheader("Model & Parameter Notes")

    st.info(
        f"**Note on Spike Reset Parameters:**\n\n"
        f"• **Spike Peak Threshold (V_peak):** Currently set to **{V_peak} mV**.\n"
        f"• **Post-Spike Reset Voltage (V_reset):** Currently set to **{V_reset} mV**.\n\n"
        "These default reset boundaries maintain numerical stability across differential integration steps."
    )

st.divider()

# Simulation & Visualization Section
if generate_btn or "sim_done" in st.session_state:
    st.session_state["sim_done"] = True

    try:
        # Run AdEx Numerical Simulation
        sim_data = simulate_adex(
            params=active_params,
            duration_ms=duration_ms,
            dt=dt_ms,
            V_peak=V_peak,
            V_reset=V_reset
        )

        time = sim_data["time"]
        V = sim_data["V"]
        w = sim_data["w"]
        spike_times = sim_data["spike_times"]

        # Run Analysis
        metrics = analyze_firing_pattern(spike_times, duration_ms)

        # Display Metrics Dashboard Cards
        st.subheader("Simulation & Firing Pattern Analysis")

        m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
        m_col1.metric("Detected Spikes", metrics["num_spikes"])
        m_col2.metric("Mean Frequency", f"{metrics['mean_frequency_hz']} Hz")
        m_col3.metric("Mean ISI", f"{metrics['mean_isi_ms'] if metrics['mean_isi_ms'] else 'N/A'} ms")
        m_col4.metric("ISI CV", metrics['cv_isi'] if metrics['cv_isi'] is not None else 'N/A')
        m_col5.metric("Firing Pattern", metrics["firing_mode"])

        st.divider()

        # Plotting Membrane Potential and Adaptation Current
        st.subheader("Membrane Potential Trace V(t)")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 6), sharex=True, gridspec_kw={'height_ratios': [2.5, 1]})

        # Subplot 1: Membrane Potential V(t)
        ax1.plot(time, V, color="#D32F2F", linewidth=1.2, label="V(t) Membrane Potential")
        ax1.axhline(active_params["VT"], color="#757575", linestyle="--", linewidth=1.0, label=f"VT ({active_params['VT']} mV)")
        ax1.axhline(active_params["EL"], color="#388E3C", linestyle=":", linewidth=1.0, label=f"EL ({active_params['EL']} mV)")
        ax1.set_ylabel("Membrane Potential (mV)", fontsize=11, fontweight="bold")
        ax1.set_title(f"Electrophysiological Firing Trace - {active_params['name']} (I = {active_params['I']} pA)", fontsize=13, fontweight="bold")
        ax1.grid(True, linestyle=":", alpha=0.6)
        ax1.legend(loc="upper right", frameon=True)

        # Subplot 2: Adaptation Current w(t)
        ax2.plot(time, w, color="#1976D2", linewidth=1.2, label="w(t) Adaptation Current")
        ax2.set_xlabel("Time (ms)", fontsize=11, fontweight="bold")
        ax2.set_ylabel("Adaptation w (pA)", fontsize=11, fontweight="bold")
        ax2.grid(True, linestyle=":", alpha=0.6)
        ax2.legend(loc="upper right", frameon=True)

        plt.tight_layout()
        st.pyplot(fig)

        # Download / Data Export Section
        st.caption("Data Export: Export simulation time series to CSV for external analysis.")
        df_export = pd.DataFrame({"Time_ms": time, "MembranePotential_mV": V, "AdaptationCurrent_pA": w})
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Simulation Data (CSV)",
            data=csv_data,
            file_name=f"{selected_neuron_key.split()[0]}_simulation_data.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Simulation Error: {str(e)}")
        st.exception(e)
else:
    st.info("Select parameters in the sidebar and click Generate Firing Pattern to start the simulation.")
