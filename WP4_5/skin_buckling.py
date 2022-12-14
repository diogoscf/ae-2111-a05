import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

import design_options
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

def skin_mos_calc(Cld, ptloads, distloads, load_factor, dynp, yspace=y_vals, wbox = WINGBOX):
    sigma_vals = stresses_along_wing(Cld, ptloads, distloads, load_factor, dynp, yspace, wbox)[:, 0]
    ribs = wbox["ribs"]
    mos_vals = []
    for rstart, rend in zip(ribs, ribs[1:]):
        stringers_top, stringers_bottom = stringers((rstart+rend)/2, wbox)
        nstringers = len([*stringers_top, *stringers_bottom])
        #print(nstringers)
        max_width = chord_y(rstart) * 0.45 / nstringers if nstringers > 0 else chord_y(rstart) * 0.45
        crit = sigma_crit_skin(wbox["skin_thickness"], max_width)
        idx_start, idx_end = (np.floor((rstart * points))), np.ceil((rend * points)) - 1
        max_stress = np.min(sigma_vals[int(idx_start):int(idx_end)]) # Negative stresses
        mos = abs(crit*1e-6 / max_stress)
        mos_vals.append([rstart*halfspan, rend*halfspan, mos])
        #print(rstart*halfspan, rend*halfspan, mos, max_stress, crit*1e-6)
    
    return mos_vals

def plot_mos_vals(mos_list, ax = False, graphlabel = "", colour = "blue", logscale = False, title = "Margin of Safety Along Wing Span"):
    if not ax:
        fig, ax = plt.subplots()
    x_vals = []
    y_vals = []
    for mos in mos_list:
        x_vals.extend([mos[0], mos[1]])
        y_vals.extend([mos[2], mos[2]])
    
    ax.plot(x_vals, y_vals, label = graphlabel, color = colour)
    if logscale:
        ax.set_yscale("log")
        ax.yaxis.set_major_formatter(ScalarFormatter())
    if not ax:
        plt.title(title)
        plt.xlabel("y [m]")
        plt.ylabel("MoS")
        plt.grid()

if __name__ == "__main__":
    fig, ax = plt.subplots()

    # Old Options
    # Design Option 1
    # mos_vals = skin_mos_calc(CL_d, point_loads, distributed_loads, load_factor, dynp, wbox=design_options.option_1)
    # plot_mos_vals(mos_vals, ax, "Design Option 1")

    # Design Option 2
    # mos_vals = skin_mos_calc(CL_d, point_loads, distributed_loads, load_factor, dynp, wbox=design_options.option_2)
    # plot_mos_vals(mos_vals, ax, "Design Option 2")

    # Design Option 2
    # mos_vals = skin_mos_calc(CL_d, point_loads, distributed_loads, load_factor, dynp, wbox=design_options.option_3)
    # plot_mos_vals(mos_vals, ax, "Design Option 3")

    # New Options

    mos_vals = skin_mos_calc(CL_d, point_loads, distributed_loads, load_factor, dynp, wbox=design_options.option_new_2)
    plot_mos_vals(mos_vals, ax, f"Load Factor: {load_factor}", "blue", True)
    print(f"Option 1: {np.min(np.array(mos_vals)[:,2])}")

    mos_vals = skin_mos_calc(2.27, point_loads, distributed_loads, -1.5, 3331.298316, wbox=design_options.option_new_2)
    plot_mos_vals(mos_vals, ax, f"Load Factor: {-1.5}", "green", True)

    # mos_vals = skin_mos_calc(CL_d, point_loads, distributed_loads, load_factor, dynp, wbox=design_options.option_new_2)
    # plot_mos_vals(mos_vals, ax, "Design Option 2", "green", True)
    # print(f"Option 2: {np.min(np.array(mos_vals)[:,2])}")

    ax.axhline(1, color="k", ls="--")
    ax.set(xlabel="y [m]", ylabel="MoS")
    ax.set_xlim(0, 22)
    ax.legend()
    ax.grid()

    plt.show()