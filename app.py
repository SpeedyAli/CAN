import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

st.set_page_config(page_title="T-x-y and x-y Diagrams - Hexane-Heptane", layout="centered")
st.title("T-x-y and x-y Diagram Analysis for Hexane-Heptane Mixture")

st.markdown("""
**Submitted by**: Nauman Salman Zafar  
**To:** Prof. Imran Mohammad  
**Department of Petrochemical**  
**UIT RGPV, Bhopal**

---

### System Studied: n-Hexane + n-Heptane

This app calculates and plots T-x-y and x-y diagrams for an ideal binary mixture using Raoult's Law and Antoine's Equation.
""")

antoine_constants = {
    "heptane": {'A': 6.893, 'B': 1260.0, 'C': 216.0},
    "hexane": {'A': 6.8763, 'B': 1171.53, 'C': 224.366}
}

def antoine_eq(T, A, B, C):
    return 10**(A - B / (C + T))

P_total = 760

def bubble_point_temp(x_heptane):
    def func(T):
        P_heptane = antoine_eq(T, **antoine_constants["heptane"])
        P_hexane = antoine_eq(T, **antoine_constants["hexane"])
        x_hexane = 1 - x_heptane
        return x_heptane * P_heptane + x_hexane * P_hexane - P_total
    return fsolve(func, 80)[0]

x_vals = np.linspace(0, 1, 21)
T_vals = []
y_vals = []

for x in x_vals:
    T = bubble_point_temp(x)
    P_heptane = antoine_eq(T, **antoine_constants["heptane"])
    y = (x * P_heptane) / P_total
    T_vals.append(T)
    y_vals.append(y)

fig1, ax1 = plt.subplots()
ax1.plot(x_vals, T_vals, label='Liquid (x vs T)', marker='o')
ax1.plot(y_vals, T_vals, label='Vapor (y vs T)', marker='s')
ax1.set_xlabel('Mole Fraction of Heptane')
ax1.set_ylabel('Temperature (°C)')
ax1.set_title('T-x-y Diagram for Hexane-Heptane')
ax1.legend()
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot(x_vals, y_vals, marker='d', label='x-y Curve')
ax2.plot([0, 1], [0, 1], '--', label='y = x')
ax2.set_xlabel('Liquid Mole Fraction of Heptane (x)')
ax2.set_ylabel('Vapor Mole Fraction of Heptane (y)')
ax2.set_title('x-y Diagram for Hexane-Heptane')
ax2.legend()
st.pyplot(fig2)

st.markdown("### Notes")
st.markdown("""
- Antoine Equation:  
  $$P_{\\text{sat}} = 10^{A - \\frac{B}{C + T}}$$

- Bubble point temperature:  
  $$x_1 P_1^{sat} + x_2 P_2^{sat} = P_{\\text{total}}$$
""")

st.latex(r"y = \frac{x_1 P_1^{sat}}{P_{total}}")

st.markdown("""
This app is useful for visualizing VLE behavior of a non-azeotropic binary system.

""")
