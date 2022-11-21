import numpy as np
import scipy as sp
from scipy import integrate
from scipy import interpolate
import Distributions
import matplotlib.pyplot as plt
from math import pi


def shear_force_calc(cl_d, point_loads):
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


def shear_force_diagram(cl_d, point_loads=[(0, 0)]):
    y_pos = np.linspace(0, 22, 300)
    shear_force = shear_force_calc(cl_d, point_loads)
    plt.plot(y_pos, shear_force)
    plt.title(f"Shear force at a cl of {cl_d}")
    plt.show()


def moment_diagram(cl_d, point_loads=[(0, 0)]):
    y_tab = []
    f_tab = []
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
    plt.plot(y_pos, y_tab)
    plt.title(f"Moment at a cl of {cl_d}")
    plt.show()


if __name__ == "__main__":
    moment_diagram(1)
