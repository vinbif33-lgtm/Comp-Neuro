# Computational Neuronal Firing Pattern Library

A modular computational neuroscience library and GUI application built in Python and Streamlit to simulate canonical neuronal firing dynamics using the **Adaptive Exponential Integrate-and-Fire (AdEx)** model.

---

## 1. Project Architecture

The project follows a clean separation of backend numerical simulation logic and frontend user interface:

```text
neuron_library/
├── app.py              # Streamlit GUI application (Frontend)
├── models.py           # AdEx differential equation integration engine
├── parameters.py       # Cerebellar neuronal electrophysiological database
├── analysis.py         # Spike detection, ISI, and firing frequency metrics
├── test_simulation.py  # Standalone backend validation & unit testing script
├── requirements.txt    # Project dependencies
└── README.md           # Documentation and setup instructions
```

---

## 2. AdEx Mathematical Model

The Adaptive Exponential Integrate-and-Fire (AdEx) model describes membrane potential dynamics \(V(t)\) coupled with a slow adaptation current \(w(t)\):

$$\begin{aligned}
C \frac{dV}{dt} &= -g_L (V - E_L) + g_L \Delta_T \exp\left( \min\left(\frac{V - V_T}{\Delta_T}, 20\right) \right) - w + I \\[6pt]
\tau_w \frac{dw}{dt} &= a (V - E_L) - w
\end{aligned}$$

### Spike Reset Rule
When \(V(t) \ge V_{\text{peak}}\):
1. A spike timestamp \(t_{\text{spike}}\) is recorded.
2. Membrane potential is reset: \(V \to V_{\text{reset}}\).
3. Adaptation current is incremented: \(w \to w + b\).

---

## 3. Electrophysiological Parameter Conventions & Units

| Parameter Symbol | Parameter Name | Standard Unit | GrC Baseline Value |
| :---: | :--- | :---: | :---: |
| **C** | Membrane Capacitance | pF | 1.0 |
| **gL** | Leak Conductance | nS | 10.0 |
| **EL** | Reversal Potential | mV | -70.0 |
| **\(\Delta_T\)** | Exponential Slope Factor | mV | 2.0 |
| **VT** | Spike Threshold Parameter | mV | -50.0 |
| **\(\tau_w\)** | Adaptation Time Constant | ms | 0.71 |
| **I** | Applied Injected Current | pA | 20.0 |
| **a** | Subthreshold Adaptation Coupling | nS | -10.0 |
| **b** | Spike-Triggered Adaptation Increment | pA | 265.0 |

---

## 4. Setup & Running Instructions

### Step 1: Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Step 2: Test the Backend Simulation Engine
```bash
python test_simulation.py
```

### Step 3: Launch the Streamlit Graphical Interface
```bash
python -m streamlit run app.py
```

---

## 5. Multi-Neuron Library Expansion

The library includes parameter sets for cerebellar neuronal populations:
- **GrC**: Cerebellar Granule Cell
- **GoC**: Golgi Cell
- **PC**: Purkinje Cell
- **IO**: Inferior Olive Cell
- **DCN**: Deep Cerebellar Nuclei
