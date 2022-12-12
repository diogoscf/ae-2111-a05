import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import interpolate

from params import *
from stiffness import airfoil_info, chord_y, MOI, stringers, thickness_y
from diagrams import moment_calc
from deflections import plot_diagram_threshold

rel = lambda y: y / (WING["span"] / 2)

CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
point_loads = CRIT["point_loads"]
point_torques = CRIT["point_torques"]
distributed_loads = CRIT["distributed_loads"]
dynp = CRIT["dynp"]
points = 300

y_vals = np.linspace(0, WING["span"] / 2, points)

def stresses_along_wing(Cld, ptloads, distloads, load_factor, dynp, yspace=y_vals):
    m_vals = moment_calc(Cld, ptloads, distloads, load_factor, dynp, yspace)
    m_estimate = sp.interpolate.interp1d(
        yspace, m_vals, kind="cubic", fill_value="extrapolate"
    )

    Ixx_vals = np.array([MOI(rel(y))[0] for y in yspace])
    Ixx_estimate = sp.interpolate.interp1d(
        yspace, Ixx_vals, kind="cubic", fill_value="extrapolate"
    )

    sigma_vals = np.array([sigma_y(y, m_estimate(y), Ixx_estimate(y)) for y in yspace])

    return sigma_vals

# y is the relative value (y/(b/2))
def area(y):
    area = 0
    chord = chord_y(y)
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
    t_spar = thickness_y(y, *WINGBOX["spar_thickness"])
    for i, s in enumerate(spars):
        area += airfoil_info(s)[0] * chord * t_spar
        if i < len(spars) - 1:
            start, end = s, spars[i+1]
            z_start, z_end = airfoil_info(s)[2:], airfoil_info(end)[2:]
            l_u = np.sqrt((end - start)**2 + (z_start[0] - z_end[0])**2)
            l_l = np.sqrt((end - start)**2 + (z_start[1] - z_end[1])**2)
            area += (l_u + l_l) * chord * WINGBOX["skin_thickness"]
    
    stringers_top, stringers_bottom = stringers(y)
    nstringers = len([*stringers_top, *stringers_bottom])
    area += nstringers * WINGBOX["stringer_area"]
    return area


# Returns maximum compressive and tensile stresses at a given y value (sigma_compressive, sigma_tensile)
def sigma_y(y, M, Ixx):
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(rel(y))]])
    chord = chord_y(rel(y))
    dists = [[*airfoil_info(s)[2:]] for s in spars]
    max_pos = max([d[0] for d in dists])*chord
    min_pos = min([d[1] for d in dists])*chord

    axial_load = -375000 * np.sin(WING["LE_sweep"]) if y < 8.374 else 0 # Compressive
    axial_stress = (axial_load / area(rel(y)))*(1e-6)

    if M < 0:
        return (M*max_pos*(1e-6)/Ixx)+axial_stress, (M*min_pos*(1e-6)/Ixx)+axial_stress
    else:
        return (M*min_pos*(1e-6)/Ixx)+axial_stress, (M*max_pos*(1e-6)/Ixx)+axial_stress
    

if __name__ == "__main__":
    sigma_vals = stresses_along_wing(CL_d, point_loads, distributed_loads, load_factor, dynp)
    plot_diagram_threshold(
        y_vals,
        sigma_vals[:,0],
        MAT["sigma_y"]*1e-6,
        "y (m)",
        "σ (MPa)",
        f"Maximum Compressive Stress along wing span at load factor {load_factor}",
    )
    plt.show()