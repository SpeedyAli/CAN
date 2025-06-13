import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Page setup
st.set_page_config(page_title="T-x-y and x-y Diagrams - Nauman Salman Zafar", layout="centered")
st.title("T-x-y and x-y Diagram Analysis for acetylene-n-heptane Mixture")

st.markdown("""
**Submitted by**: Nauman Salman Zafar  
**To:** Prof. Imran Mohammad  
**Department of Petrochemical**  
**UIT RGPV, Bhopal**

---
### Assignment Overview
This assignment demonstrates the calculation and plotting of **T-x-y** and **x-y diagrams** for an ideal binary mixture (heptane + octane) using:
- **Raoult’s Law**
- **Antoine Equation**

These diagrams are useful in understanding phase behavior in distillation.

---
### 1. Antoine Equation
Used to calculate the **saturation pressure (Psat)** of each component:

\[log10(Psat) = A - (B)/(C + T)\]

Where:
- T is temperature in °C
- Psat is in mmHg

Antoine constants used:
- **Acetylene**: A = 6.81228, B = 625.64, C = 255.0
- **n-Heptane**: A = 6.893, B = 1260, C = 216


---
### 2. T-x-y Diagram (Temperature vs Mole Fractions)
#### How it is calculated:
1. For each liquid mole fraction \( x \) of heptane, calculate the bubble point temperature \( T \) by solving:
   \[P total = x_H * P_H^*(T) + x_O * P_O^*(T)\] 
2. Then calculate vapor mole fraction \( y \):
            
   \[y_H = (x_H * P_H^*(T))/(P_total)\]
            
   \[y_O = 1 - y_H\]  
            
   \[P total = 760 mmhg\]
            
3. Plot T vs x and T vs y.

---
### 3. x-y Diagram (Vapor vs Liquid Mole Fraction)
#### How it is calculated:
Once we calculate mole fraction \( x \) in liquid and corresponding \( y \) in vapor (from the T-x-y data), we simply:
- Plot \( x \) on X-axis
- Plot \( y \) on Y-axis
- Include diagonal reference line (y = x) for comparison

This helps understand the separation behavior in distillation.

---
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
