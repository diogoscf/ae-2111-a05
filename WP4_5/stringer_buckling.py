import numpy as np
import matplotlib.pyplot as plt

from params import *
from stresses import stresses_along_wing
import design_options

CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
point_loads = CRIT["point_loads"]
point_torques = CRIT["point_torques"]
distributed_loads = CRIT["distributed_loads"]
dynp = CRIT["dynp"]
points = 300

y_vals = np.linspace(0, WING["span"] / 2, points)

K = 4

stringer = { # L-shaped
    "height": 60e-3, # meter
    "width": 60e-3, # meter
    "thickness": 6e-3, # meter
}

def maxlength(stress, K, E, I, A):
    return np.sqrt(K * (np.pi**2) * E * I / (abs(stress) * A))

if __name__ == "__main__":
    wbox = design_options.option_new_2
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

