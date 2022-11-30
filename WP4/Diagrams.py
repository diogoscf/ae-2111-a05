import numpy as np
import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
from math import pi

import Distributions
from params import *

G = 9.80665
halfspan = WING["span"] / 2
y_space = np.linspace(0, halfspan, 300)
wing_mass = (-199.8707 * G, 4355.183221 * G)
engine_mass = (7277 * G, 8.374)
engine_thrust = (375000 * 2, 8.374)


def shear_force_calc(
    cl_d,
    point_loads=[],
    distributed_loads=[],
    load_factor=1,
    dyn_p=10000,
    y_pos=y_space,
):
    f_tab = []
    normal = Distributions.N_prime(cl_d, (0.028 + cl_d**2 / (pi * 10 * 0.51)), y_pos, dyn_p)
    function = sp.interpolate.interp1d(y_pos, normal, kind="cubic", fill_value="extrapolate")
    for y in y_pos:
        estimate_f, _ = sp.integrate.quad(function, y, y_pos[-1])
        estimate_f *= load_factor
        for load, pos in point_loads:
            if y <= pos:
                estimate_f -= load * load_factor
        for a, b in distributed_loads:
            estimate_f -= (a * y + b) * load_factor
        f_tab.append(-estimate_f)
    return f_tab


def shear_force_diagram(
    cl_d,
    point_loads=[],
    distributed_loads=[wing_mass],
    load_factor=1,
    dyn_p=10000,
    y_pos=y_space,
):
    shear_force = shear_force_calc(cl_d, point_loads, distributed_loads, load_factor, dyn_p, y_pos)
    plt.plot(y_pos, shear_force)
    plt.title(f"Shear force at cl: {cl_d} n: {load_factor}, and dyn_p: {round(dyn_p, 1)}")
    plt.xlabel("y [m]")
    plt.ylabel("Shear force [N]")
    plt.show()


def moment_calc(
    cl_d,
    point_loads=[],
    distributed_loads=[],
    load_factor=1,
    dyn_p=10000,
    y_pos=y_space,
):
    y_tab = []
    function_m = sp.interpolate.interp1d(
        y_pos,
        shear_force_calc(cl_d, point_loads, distributed_loads, load_factor, dyn_p, y_pos),
        kind="cubic",
        fill_value="extrapolate",
    )
    for y in y_pos:
        estimate_m, _ = sp.integrate.quad(function_m, y, y_pos[-1])
        y_tab.append(estimate_m)

    return y_tab


def moment_diagram(
    cl_d,
    point_loads=[],
    distributed_loads=[],
    load_factor=1,
    dyn_p=10000,
    y_pos=y_space,
):
    moments = moment_calc(cl_d, point_loads, distributed_loads, load_factor, dyn_p, y_pos)
    plt.plot(y_pos, moments)
    plt.title(f"Moment at cl: {cl_d}, n: {load_factor}, and dyn_p: {round(dyn_p, 1)}")
    plt.xlabel("y [m]")
    plt.ylabel("Moment [Nm]")
    plt.show()


def distance_flexural_axis(y):
    chord_y = lambda y: (((WING["taper_ratio"] - 1) / (halfspan)) * abs(y) + 1) * WING["root_chord"]
    return chord_y(y) / 4


def torque_calc(cl_d, point_loads=[], load_factor=1, dyn_p=10000, y_pos=y_space):
    t_tab = []
    normal = Distributions.N_prime(cl_d, (0.028 + cl_d**2 / (pi * 10 * 0.51)), y_pos, dyn_p)
    intpl = sp.interpolate.interp1d(y_pos, normal, kind="cubic", fill_value="extrapolate")
    function = lambda y: intpl(y) * distance_flexural_axis(y)
    for y in y_pos:
        estimate_t, _ = sp.integrate.quad(function, y, y_pos[-1])
        estimate_t *= load_factor
        for load, pos in point_loads:
            if y <= pos:
                estimate_t += load
        t_tab.append(estimate_t)
    return t_tab


def torque_diagram(cl_d, point_loads=[], load_factor=1, dyn_p=10000, y_pos=y_space):
    torque = torque_calc(cl_d, point_loads, load_factor, dyn_p, y_pos)
    plt.plot(y_pos, torque)
    plt.title(f"Torque at cl: {cl_d}, n: {load_factor}, and dyn_p: {round(dyn_p, 1)}")
    plt.xlabel("y [m]")
    plt.ylabel("Torque [Nm]")
    plt.show()


if __name__ == "__main__":
    shear_force_diagram(0.908, [engine_mass], [wing_mass], 3.75, 3703.338805)
    shear_force_diagram(0.908, [engine_mass], [wing_mass], 3.75, 8328.245793)
    shear_force_diagram(0.908, [engine_mass], [wing_mass], 3.75, 4838.801824)
    shear_force_diagram(2.27, [engine_mass], [wing_mass], -1.5, 1481.335522)
    shear_force_diagram(2.27, [engine_mass], [wing_mass], -1.5, 3331.298316)
    shear_force_diagram(2.27, [engine_mass], [wing_mass], -1.5, 1935.52073)
    moment_diagram(0.908, [engine_mass], [wing_mass], 3.75, 3703.338805)
    moment_diagram(0.908, [engine_mass], [wing_mass], 3.75, 8328.245793)
    moment_diagram(0.908, [engine_mass], [wing_mass], 3.75, 4838.801824)
    moment_diagram(2.27, [engine_mass], [wing_mass], -1.5, 1481.335522)
    moment_diagram(2.27, [engine_mass], [wing_mass], -1.5, 3331.298316)
    moment_diagram(2.27, [engine_mass], [wing_mass], -1.5, 1935.52073)
    torque_diagram(0.908, [engine_thrust], 3.75, 3703.338805)
    torque_diagram(0.908, [engine_thrust], 3.75, 8328.245793)
    torque_diagram(0.908, [engine_thrust], 3.75, 4838.801824)
    torque_diagram(2.27, [], -1.5, 1481.335522)
    torque_diagram(2.27, [], -1.5, 3331.298316)
    torque_diagram(2.27, [], -1.5, 1935.52073)
    # print(shear_force_calc(0.908, [engine_mass], [wing_mass], 3.75, 3703.338805)[0])
    # print(shear_force_calc(0.908, [engine_mass], [wing_mass], 3.75, 8328.245793)[0])
    # print(shear_force_calc(0.908, [engine_mass], [wing_mass], 3.75, 4838.801824)[0])
    # print(shear_force_calc(2.27, [engine_mass], [wing_mass], -1.5, 1481.335522)[0])
    # print(shear_force_calc(2.27, [engine_mass], [wing_mass], -1.5, 3331.298316)[0])
    # print(shear_force_calc(2.27, [engine_mass], [wing_mass], -1.5, 1935.52073)[0])
    # print(moment_calc(0.908, [engine_mass], [wing_mass], 3.75, 3703.338805)[0])
    # print(moment_calc(0.908, [engine_mass], [wing_mass], 3.75, 8328.245793)[0])
    # print(moment_calc(0.908, [engine_mass], [wing_mass], 3.75, 4838.801824)[0])
    # print(moment_calc(2.27, [engine_mass], [wing_mass], -1.5, 1481.335522)[0])
    # print(moment_calc(2.27, [engine_mass], [wing_mass], -1.5, 3331.298316)[0])
    # print(moment_calc(2.27, [engine_mass], [wing_mass], -1.5, 1935.52073)[0])
    # print(torque_calc(0.908, [engine_thrust], 3.75, 3703.338805)[0])
    # print(torque_calc(0.908, [engine_thrust], 3.75, 8328.245793)[0])
    # print(torque_calc(0.908, [engine_thrust], 3.75, 4838.801824)[0])
    # print(torque_calc(2.27, [], -1.5, 1481.335522)[0])
    # print(torque_calc(2.27, [], -1.5, 3331.298316)[0])
    # print(torque_calc(2.27, [], -1.5, 1935.52073)[0])
#
