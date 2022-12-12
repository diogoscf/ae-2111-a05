import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import interpolate

import sys
import os

sys.path.insert(1, os.path.join(os.path.dirname(__file__), "../WP4/"))

from params import *
from stiffness import *
from diagrams import moment_calc
from deflections import *

sigma_yield = 276e6

def plot_stresses(Cld, ptloads, distloads, load_factor, dynp, yspace=y_vals):
    m_vals = moment_calc(Cld, ptloads, distloads, load_factor, dynp, yspace)
    m_estimate = sp.interpolate.interp1d(
        yspace, m_vals, kind="cubic", fill_value="extrapolate"
    )

    Ixx_vals = np.array([stiffness.MOI(rel(y))[0] for y in yspace])
    Ixx_estimate = sp.interpolate.interp1d(
        yspace, Ixx_vals, kind="cubic", fill_value="extrapolate"
    )

    sigma_vals = np.array([sigma_y(y, m_estimate(y), Ixx_estimate(y)) for y in yspace])
    
    #print(v_vals[-1], f"{100*v_vals[-1]/WING['span']:.2f}%")
    plot_diagram_threshold(
        y_vals,
        sigma_vals[:,0],
        sigma_yield*1e-6,
        "y (m)",
        "σ (Pa)",
        f"Maximum Compressive Stress along wing span at load factor {load_factor}",
    )

# Returns maximum compressive and tensile stresses at a given y value (sigma_compressive, sigma_tensile)
def sigma_y(y, M, Ixx):
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(rel(y))]])
    chord = chord_y(rel(y))
    dists = [[*airfoil_info(s)[2:]] for s in spars]
    max_pos = max([d[0] for d in dists])*chord
    min_pos = min([d[1] for d in dists])*chord

    if M < 0:
        return M*max_pos*(1e-6)/Ixx, M*min_pos*(1e-6)/Ixx
    else:
        return M*min_pos*(1e-6)/Ixx, M*max_pos*(1e-6)/Ixx
    

if __name__ == "__main__":
    plot_stresses(CL_d, point_loads, distributed_loads, load_factor, dynp)
    plt.show()