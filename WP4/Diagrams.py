import numpy as np
import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
from math import pi

import Distributions
from params import *

def shear_force_calc(cl_d, point_loads=[]):
    f_tab = []
    y_pos = np.linspace(0, 22, 300)
    normal = Distributions.N_prime(
        cl_d, (0.028 + cl_d**2 / (pi * 10 * 0.51)), y_pos, 10000
    )
    function = sp.interpolate.interp1d(
        y_pos, normal, kind="cubic", fill_value="extrapolate"
    )
    for y in y_pos:
        estimate_f, _ = sp.integrate.quad(function, y, y_pos[-1])
        for load, pos in point_loads:
            if y <= pos:
                estimate_f -= load
        f_tab.append(-estimate_f)
    return f_tab


def shear_force_diagram(cl_d, point_loads=[]):
    y_pos = np.linspace(0, 22, 300)
    shear_force = shear_force_calc(cl_d, point_loads)
    plt.plot(y_pos, shear_force)
    plt.title(f"Shear force at a cl of {cl_d}")
    plt.show()

def moment_calc(cl_d, point_loads=[]):
    y_tab = []
    y_pos = np.linspace(0, 22, 300)
    function_m = sp.interpolate.interp1d(
        y_pos,
        shear_force_calc(cl_d, point_loads),
        kind="cubic",
        fill_value="extrapolate",
    )
    for y in y_pos:
        estimate_m, _ = sp.integrate.quad(function_m, y, y_pos[-1])
        y_tab.append(estimate_m)
    
    return y_tab


def moment_diagram(cl_d, point_loads=[]):
    y_pos = np.linspace(0, 22, 300)
    moments = moment_calc(cl_d, point_loads)
    plt.plot(y_pos, moments)
    plt.title(f"Moment at a cl of {cl_d}")
    plt.show()


def distance_flexural_axis(y_pos):
    root_chord = WING["root_chord"]
    tip_chord = WING["root_chord"] * WING["taper_ratio"]
    half_wingspan = WING["span"] / 2
    return(((tip_chord - root_chord)/(2 * half_wingspan))* y_pos + root_chord/4)


def torque_calc(cl_d, point_loads=[]):
    t_tab = []
    y_pos = np.linspace(0, 22, 300)
    normal = Distributions.N_prime(
        cl_d, (0.028 + cl_d ** 2 / (pi * 10 * 0.51)), y_pos, 10000
    )
    function = lambda y: sp.interpolate.interp1d(
        y_pos, normal, kind="cubic", fill_value="extrapolate"
    )(y) * distance_flexural_axis(y)
    for y in y_pos:
        estimate_t, _ = sp.integrate.quad(function, y, y_pos[-1])
        for load, pos in point_loads:
            if y <= pos:
                estimate_t += load
        t_tab.append(-estimate_t)
    return t_tab

def torque_diagram(cl_d, point_loads=[]):
    y_pos = np.linspace(0, 22, 300)
    torque = torque_calc(cl_d, point_loads)
    plt.plot(y_pos, torque)
    plt.title(f"Torque at a cl of {cl_d}")
    plt.show()

if __name__ == "__main__":
    moment_diagram(1)
    torque_diagram(1, [(35000, 8.374)])