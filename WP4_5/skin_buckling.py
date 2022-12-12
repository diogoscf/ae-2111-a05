import numpy as np
from stresses import stresses_along_wing
from params import *
from stiffness import chord_y, stringers

k_c = 4  # based on four simply supported edges and an a/b of >3
E = MAT["E"]
nu = MAT["nu"]
halfspan = WING["span"] / 2

rel = lambda y: y / (WING["span"] / 2)

CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
point_loads = CRIT["point_loads"]
point_torques = CRIT["point_torques"]
distributed_loads = CRIT["distributed_loads"]
dynp = CRIT["dynp"]
points = 300

y_vals = np.linspace(0, WING["span"] / 2, points)

# Critical Buckling Stress
def sigma_crit_skin(t, b):
    return ((np.pi**2) * k_c * E / (12 * (1 - (nu**2)))) * ((t / b)**2)

def skin_mos_calc(Cld, ptloads, distloads, load_factor, dynp, yspace=y_vals):
    sigma_vals = stresses_along_wing(Cld, ptloads, distloads, load_factor, dynp, yspace)[:, 0]
    ribs = WINGBOX["ribs"]
    mos_vals = []
    for rstart, rend in zip(ribs, ribs[1:]):
        stringers_top, stringers_bottom = stringers(rstart)
        nstringers = len([*stringers_top, *stringers_bottom])
        max_width = chord_y(rstart) * 0.45 / nstringers
        crit = sigma_crit_skin(WINGBOX["skin_thickness"], max_width)
        idx_start, idx_end = (np.floor((rstart * points))), np.ceil((rend * points)) - 1
        max_stress = np.max(sigma_vals[int(idx_start):int(idx_end)])
        mos = abs(crit*1e-6 / max_stress)
        mos_vals.append([rstart*halfspan, rend*halfspan, mos])
    
    return mos_vals
if __name__ == "__main__":
    print(skin_mos_calc(CL_d, point_loads, distributed_loads, load_factor, dynp))