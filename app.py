import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# App setup
st.set_page_config(page_title="VLE Diagrams - Acetylene and n-Heptane", layout="centered")
st.title("T-x-y and x-y Diagram for Acetylene + n-Heptane System")

st.markdown("""
#### Submitted by: **Mohd Ali Khan**  
**To:** Prof. Imran Mohammad  
**Department of Petrochemical Engineering**  
**UIT RGPV, Bhopal**

---

### System Studied: Acetylene + n-Heptane

This app calculates and plots T-x-y and x-y diagrams for an ideal binary mixture using Raoult's Law and Antoine Equation.
""")

# Antoine constants
antoine_constants = {
    "acetylene": {"A": 6.81228, "B": 625.64, "C": 255.0},
    "n-heptane": {"A": 6.893, "B": 1260.0, "C": 216.0}
}

def antoine_eq(T, A, B, C):
    return 10**(A - B / (C + T))  # P in mmHg

P_total = 760  # Total pressure in mmHg

def bubble_point_temp(x_acetylene):
    def func(T):
        P_a = antoine_eq(T, **antoine_constants["acetylene"])
        P_h = antoine_eq(T, **antoine_constants["n-heptane"])
        x_h = 1 - x_acetylene
        return x_acetylene * P_a + x_h * P_h - P_total
    return fsolve(func, 60)[0]  # Start guess from 60°C

# Generate data
x_vals = np.linspace(0, 1, 21)
T_vals = []
y_vals = []

for x in x_vals:
    T = bubble_point_temp(x)
    P_a = antoine_eq(T, **antoine_constants["acetylene"])
    y = (x * P_a) / P_total
    T_vals.append(T)
    y_vals.append(y)

# T-x-y Diagram
st.subheader("T-x-y Diagram")
fig1, ax1 = plt.subplots()
ax1.plot(x_vals, T_vals, 'bo-', label='Liquid (x vs T)')
ax1.plot(y_vals, T_vals, 'ro--', label='Vapor (y vs T)')
ax1.set_xlabel("Mole Fraction of Acetylene")
ax1.set_ylabel("Temperature (°C)")
ax1.set_title("T-x-y Diagram at 1 atm")
ax1.legend()
ax1.grid()
st.pyplot(fig1)

# x-y Diagram
st.subheader("x-y Diagram")
fig2, ax2 = plt.subplots()
ax2.plot(x_vals, y_vals, 'go-', label='x-y Curve')
ax2.plot([0, 1], [0, 1], 'k--', label='y = x')
ax2.set_xlabel("x (Liquid Mole Fraction of Acetylene)")
ax2.set_ylabel("y (Vapor Mole Fraction of Acetylene)")
ax2.set_title("x-y Diagram at 1 atm")
ax2.legend()
ax2.grid()
st.pyplot(fig2)

st.markdown("""
---

### Notes:
- Antoine Equation:  \( P_{\text{sat}} = 10^{A - B / (C + T)} \)
- Bubble point T: Solve \( x_a P_a + (1 - x_a) P_h = P_{\text{total}} \)
- Vapor mole fraction: \( y = \frac{x P_a}{P_{\text{total}}} \)

This app is useful for visualizing VLE behavior of a non-azeotropic binary system.

""")