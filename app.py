import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

st.set_page_config(page_title="T-x-y and x-y Diagrams - Pentane-Hexane", layout="centered")
st.title("T-x-y and x-y Diagram Analysis for Pentane-Hexane Mixture")

st.markdown("""
**Submitted by**: Nauman Salman Zafar  
**To:** Prof. Imran Mohammad  
**Department of Petrochemical**  
**UIT RGPV, Bhopal**

---

### System Studied: Pentane + Hexane

This app calculates and plots T-x-y and x-y diagrams for an ideal binary mixture using Raoult's Law and Antoine's Equation.
""")

# Antoine constants for Pentane and Hexane
antoine_constants = {
    "pentane": {'A': 6.8521, 'B': 1064.84, 'C': 233.989},
    "hexane": {'A': 6.8763, 'B': 1171.53, 'C': 224.366}
}

def antoine_eq(T, A, B, C):
    return 10**(A - B / (C + T))

P_total = 760

def bubble_point_temp(x_pentane):
    def func(T):
        P_pentane = antoine_eq(T, **antoine_constants["pentane"])
        P_hexane = antoine_eq(T, **antoine_constants["hexane"])
        x_hexane = 1 - x_pentane
        return x_pentane * P_pentane + x_hexane * P_hexane - P_total
    return fsolve(func, 50)[0]

x_vals = np.linspace(0, 1, 21)
T_vals = []
y_vals = []
table_data = []

for x in x_vals:
    T = bubble_point_temp(x)
    P_pentane = antoine_eq(T, **antoine_constants["pentane"])
    y = (x * P_pentane) / P_total
    T_vals.append(T)
    y_vals.append(y)
    table_data.append((round(x, 3), round(y, 3), round(T, 2)))

fig1, ax1 = plt.subplots()
ax1.plot(x_vals, T_vals, label='Liquid (x vs T)', marker='o')
ax1.plot(y_vals, T_vals, label='Vapor (y vs T)', marker='s')
ax1.set_xlabel('Mole Fraction of Pentane')
ax1.set_ylabel('Temperature (°C)')
ax1.set_title('T-x-y Diagram for Pentane-Hexane')
ax1.legend()
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot(x_vals, y_vals, marker='d', label='x-y Curve')
ax2.plot([0, 1], [0, 1], '--', label='y = x')
ax2.set_xlabel('Liquid Mole Fraction of Pentane (x)')
ax2.set_ylabel('Vapor Mole Fraction of Pentane (y)')
ax2.set_title('x-y Diagram for Pentane-Hexane')
ax2.legend()
st.pyplot(fig2)

st.markdown("### T-x-y Table")
st.dataframe(
    {"x (Liquid Pentane)": [row[0] for row in table_data],
     "y (Vapor Pentane)": [row[1] for row in table_data],
     "T (°C)": [row[2] for row in table_data]}
)

st.markdown("### Notes")
st.markdown("**Antoine Equation:**")
st.latex(r"P_{\text{sat}} = 10^{A - \frac{B}{C + T}}")
st.markdown("**Bubble point temperature:**")
st.latex(r"x_1 P_1^{sat} + x_2 P_2^{sat} = P_{\text{total}}")

st.latex(r"y = \frac{x_1 P_1^{sat}}{P_{total}}")

st.markdown("""
This app is useful for visualizing VLE behavior of a non-azeotropic binary system.
""")
