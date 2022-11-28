import numpy as np
import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
from math import pi

import Distributions
from params import *

halfspan = WING["span"] / 2
y_space = np.linspace(0, halfspan, 300)


def shear_force_calc(cl_d, point_loads=[], load_factor=1, y_pos=y_space):
    f_tab = []
    normal = Distributions.N_prime(
        cl_d, (0.028 + cl_d**2 / (pi * 10 * 0.51)), y_pos, 10000
    )
    function = sp.interpolate.interp1d(
        y_pos, normal, kind="cubic", fill_value="extrapolate"
    )
    for y in y_pos:
        estimate_f, _ = sp.integrate.quad(function, y, y_pos[-1])
        estimate_f *= load_factor
        for load, pos in point_loads:
            if y <= pos:
                estimate_f -= load
        f_tab.append(-estimate_f)
    return f_tab


def shear_force_diagram(cl_d, point_loads=[], load_factor=1, y_pos=y_space):
    shear_force = shear_force_calc(cl_d, point_loads, load_factor, y_pos)
    plt.plot(y_pos, shear_force)
    plt.title(f"Shear force at a cl of {cl_d}")
    plt.xlabel("y [m]")
    plt.ylabel("Shear force [N]")
    plt.show()


def moment_calc(cl_d, point_loads=[], load_factor=1, y_pos=y_space):
    y_tab = []
    function_m = sp.interpolate.interp1d(
        y_pos,
        shear_force_calc(cl_d, point_loads, load_factor, y_pos),
        kind="cubic",
        fill_value="extrapolate",
    )
    for y in y_pos:
        estimate_m, _ = sp.integrate.quad(function_m, y, y_pos[-1])
        y_tab.append(estimate_m)

    return y_tab


def moment_diagram(cl_d, point_loads=[], load_factor=1, y_pos=y_space):
    moments = moment_calc(cl_d, point_loads, load_factor, y_pos)
    plt.plot(y_pos, moments)
    plt.title(f"Moment at a cl of {cl_d}")
    plt.xlabel("y [m]")
    plt.ylabel("Moment [Nm]")
    plt.show()


def distance_flexural_axis(y):
    chord_y = lambda y: (((WING["taper_ratio"] - 1)/(halfspan))*abs(y) + 1) * WING["root_chord"]
    return chord_y(y) / 4


def torque_calc(cl_d, point_loads=[], load_factor=1, y_pos=y_space):
    t_tab = []
    normal = Distributions.N_prime(
        cl_d, (0.028 + cl_d**2 / (pi * 10 * 0.51)), y_pos, 10000
    )
    intpl = sp.interpolate.interp1d(
        y_pos, normal, kind="cubic", fill_value="extrapolate"
    )
    function = lambda y: intpl(y) * distance_flexural_axis(y)
    for y in y_pos:
        estimate_t, _ = sp.integrate.quad(function, y, y_pos[-1])
        estimate_t *= load_factor
        for load, pos in point_loads:
            if y <= pos:
                estimate_t += load
        t_tab.append(estimate_t)
    return t_tab


def torque_diagram(cl_d, point_loads=[], load_factor=1, y_pos=y_space):
    torque = torque_calc(cl_d, point_loads, load_factor, y_pos)
    plt.plot(y_pos, torque)
    plt.title(f"Torque at a cl of {cl_d}")
    plt.xlabel("y [m]")
    plt.ylabel("Torque [Nm]")
    plt.show()


<<<<<<< Updated upstream
if __name__ == "__main__":
    shear_force_diagram(CRIT["cld"], CRIT["point_loads"], CRIT["load_factor"])
    # moment_diagram(1, (), 2.5)
    #torque_diagram(1, [(35000, 8.374)], 1)
    # pass
=======
#moment_diagram(1)
torque_diagram(1, [(35000, 8.374)])
>>>>>>> Stashed changes
