import numpy as np
import scipy as sp
from scipy import integrate
from scipy import interpolate
import Distributions
import matplotlib.pyplot as plt
from math import sin, cos, pi
import XFLR


def normal_force_per_span(lift_per, drag_per, angle_of_attack):
    return (
        cos(radians(angle_of_attack)) * lift_per
        + sin(radians(angle_of_attack)) * drag_per
    )


def shear_force_diagram(cl_d):
    cl_min = 0
    cl_max = 1.5
    y_tab = []
    y_pos = np.linspace(0, 22, 100)
    normal = Distributions.N_prime(
        cl_d, (0.028 + cl_d**2 / (pi * 10 * 0.51)), y_pos, 10000
    )
    function = sp.interpolate.interp1d(
        y_pos, normal, kind="cubic", fill_value="extrapolate"
    )
    for i in range(len(y_pos)):
        estimatef, _ = sp.integrate.quad(function, y_pos[i], y_pos[-1])
        y_tab.append(estimatef)
    plt.plot(y_pos, y_tab)
    plt.title(f"Shear force at a cl of {cl_d}")
    plt.show()


def moment_diagram(cl_d):
    cl_min = 0
    cl_max = 1.5
    y_tab = []
    f_tab = []
    y_pos = np.linspace(0, 22, 100)
    normal = Distributions.N_prime(
        cl_d, (0.028 + cl_d**2 / (pi * 10 * 0.51)), y_pos, 10000
    )
    function = sp.interpolate.interp1d(
        y_pos, normal, kind="cubic", fill_value="extrapolate"
    )
    for i in range(len(y_pos)):
        estimatef, _ = sp.integrate.quad(function, y_pos[i], y_pos[-1])
        f_tab.append(estimatef)
    function_m = sp.interpolate.interp1d(
        y_pos, f_tab, kind="cubic", fill_value="extrapolate"
    )
    for i in range(len(y_pos)):
        estimatem, _ = sp.integrate.quad(function_m, y_pos[i], y_pos[-1])
        y_tab.append(estimatem)

    plt.plot(y_pos, y_tab)
    plt.title(f"Moment at a cl of {cl_d}")
    plt.show()


moment_diagram(1)
