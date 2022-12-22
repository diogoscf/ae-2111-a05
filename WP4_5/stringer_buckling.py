import numpy as np
import matplotlib.pyplot as plt

from params import *
from stresses import stresses_along_wing
from skin_buckling import plot_mos_vals
import design_options

CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
point_loads = CRIT["point_loads"]
point_torques = CRIT["point_torques"]
distributed_loads = CRIT["distributed_loads"]
dynp = CRIT["dynp"]
points = 300
halfspan = WING["span"] / 2

y_vals = np.linspace(0, halfspan, points)

K = 4

stringer = { # L-shaped
    "height": 60e-3, # meter
    "width": 60e-3, # meter
    "thickness": 6e-3, # meter
}

def maxlength(stress, K, E, I, A):
    return np.sqrt(K * (np.pi**2) * E * I / (abs(stress) * A))

def find_max_length(wbox):
    cutoff = -1
    sigma_vals = stresses_along_wing(CL_d, point_loads, distributed_loads, load_factor, dynp, y_vals, wbox)[:cutoff, 0]*1e6 # Pa
    t = stringer["thickness"]
    h = stringer["height"]
    w = stringer["width"]
    area = (h+w) * t # Thin-walled
    Ixx = (t*(h**3))/12 + h*t*((h/2)**2)
    Lmax_vals = maxlength(sigma_vals, K, MAT["E"], Ixx, area)

    for rs, re in zip(wbox["ribs"], wbox["ribs"][1:]):
        L = (re - rs)*WING["span"]/2
        Lmax = np.min(Lmax_vals[int(rs*points):int(re*points)])
        print(rs, re, Lmax/L, Lmax, L)

    print(np.min(Lmax_vals))
    plt.plot(y_vals[:cutoff], Lmax_vals)
    plt.show()

def crit_stress(L):
    t = stringer["thickness"]
    h = stringer["height"]
    w = stringer["width"]
    area = (h+w) * t # Thin-walled
    Ixx = (t*(h**3))/12 + h*t*((h/2)**2)
    return K * (np.pi**2) * MAT["E"] * Ixx / (L**2 * area)

def stringer_mos_calc(Cld, ptloads, distloads, load_factor, dynp, yspace=y_vals, wbox = WINGBOX):
    sigma_vals = stresses_along_wing(Cld, ptloads, distloads, load_factor, dynp, yspace, wbox)[:, 0]
    ribs = wbox["ribs"]
    mos_vals = []
    for rstart, rend in zip(ribs, ribs[1:]):
        L = (rend - rstart) * halfspan
        crit = crit_stress(L)
        idx_start, idx_end = (np.floor((rstart * points))), np.ceil((rend * points)) - 1
        max_stress = np.max(abs(sigma_vals[int(idx_start):int(idx_end)])) # Negative stresses
        mos = abs(crit*1e-6 / max_stress)
        mos_vals.append([rstart*halfspan, rend*halfspan, mos])
        #print(rstart*halfspan, rend*halfspan, mos, max_stress, crit*1e-6)
    
    return mos_vals

if __name__ == "__main__":
    # find_max_length(design_options.option_new_2)

    fig, ax = plt.subplots()

    mos_vals = stringer_mos_calc(CL_d, point_loads, distributed_loads, load_factor, dynp, wbox=design_options.option_new_1)
    plot_mos_vals(mos_vals, ax, f"Load Factor: {load_factor}", "blue", True)

    mos_vals = stringer_mos_calc(2.27, point_loads, distributed_loads, -1.5, 3331.298316, wbox=design_options.option_new_1)
    plot_mos_vals(mos_vals, ax, f"Load Factor: {-1.5}", "green", True)

    ax.axhline(1, color="k", ls="--")
    ax.set(xlabel="y [m]", ylabel="MoS")
    ax.set_xlim(0, 22)
    ax.legend()
    ax.grid()

    plt.show()

