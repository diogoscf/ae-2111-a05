import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

import stiffness
from params import *
from Diagrams import moment_calc, torque_calc

rel = lambda y: y / (WING["span"] / 2)

CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
point_loads = CRIT["point_loads"]
point_torques = CRIT["point_torques"]
distributed_loads = CRIT["distributed_loads"]
dynp = CRIT["dynp"]
points = 300

y_vals = np.linspace(0, WING["span"] / 2, points)


def dvdy(y, M, MOI):
    result, _ = sp.integrate.quad(
        lambda x: -M(x) / (MAT["E"] * MOI(x)), 0, y, limit=100
    )
    return result


def v(y, dvdy_func):
    result, _ = sp.integrate.quad(dvdy_func, 0, y)
    return result


def theta(y, T, J):
    result, _ = sp.integrate.quad(lambda p: T(p) / (MAT["G"] * J(p)), 0, y, limit=100)
    return result


def plot_diagram_threshold(x_vals, y_vals, maxval, xlab, ylab, plottitle):
    if np.max(y_vals) < maxval and np.min(y_vals) > -maxval:
        plot_diagram(x_vals, y_vals, maxval, xlab, ylab, plottitle)
        return
    fig, ax = plt.subplots()

    cmap = ListedColormap(["blue", "red"])
    norm = BoundaryNorm([np.min(y_vals), maxval, np.max(y_vals)], cmap.N)

    points = np.array([x_vals, y_vals]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(y_vals)

    ax.add_collection(lc)
    ax.set_xlim(np.min(x_vals), np.max(x_vals))
    ax.set_ylim(np.min(y_vals) * 1.1, np.max(y_vals) * 1.1)

    ax.set(xlabel=xlab, ylabel=ylab, title=plottitle)
    ax.grid()
    if np.max(y_vals) >= maxval or (
        np.max(y_vals) > 0 and abs(np.min(y_vals)) < abs(np.max(y_vals))
    ):
        ax.axhline(maxval, color="k", ls="--")
    if np.min(y_vals) <= -maxval or (
        np.min(y_vals) < 0 and abs(np.min(y_vals)) > abs(np.max(y_vals))
    ):
        ax.axhline(-maxval, color="k", ls="--")


def plot_diagram(x_vals, y_vals, maxval, xlab, ylab, plottitle):
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, color="blue")
    ax.set(xlabel=xlab, ylabel=ylab, title=plottitle)

    if np.max(y_vals) > 0 and abs(np.min(y_vals)) < abs(np.max(y_vals)):
        ax.axhline(maxval, color="k", ls="--")
    if np.min(y_vals) < 0 and abs(np.min(y_vals)) > abs(np.max(y_vals)):
        ax.axhline(-maxval, color="k", ls="--")
    ax.grid()


def plot_deflection(Cld, ptloads, distloads, load_factor, dynp, yspace=y_vals):
    m_vals = moment_calc(Cld, ptloads, distloads, load_factor, dynp, yspace)
    m_estimate = sp.interpolate.interp1d(
        yspace, m_vals, kind="cubic", fill_value="extrapolate"
    )

    Ixx_vals = np.array([stiffness.MOI(rel(y))[0] for y in yspace])
    Ixx_estimate = sp.interpolate.interp1d(
        yspace, Ixx_vals, kind="cubic", fill_value="extrapolate"
    )

    dv_vals = np.array([dvdy(y, m_estimate, Ixx_estimate) for y in y_vals])
    dv_estimate = sp.interpolate.interp1d(
        y_vals, dv_vals, kind="cubic", fill_value="extrapolate"
    )

    v_vals = [v(y, dv_estimate) for y in y_vals]
    print(v_vals[-1], f"{100*v_vals[-1]/WING['span']:.2f}%")
    plot_diagram_threshold(
        y_vals,
        v_vals,
        0.15 * WING["span"],
        "y (m)",
        "v (m)",
        f"Deflection along wing span at load factor {load_factor}",
    )


def plot_twist(Cld, ptloads, load_factor, dynp, yspace=y_vals):
    t_vals = torque_calc(Cld, ptloads, load_factor, dynp, yspace)
    t_estimate = sp.interpolate.interp1d(
        yspace, t_vals, kind="cubic", fill_value="extrapolate"
    )

    J_vals = np.array([stiffness.torsional_constant(rel(y)) for y in yspace])
    J_estimate = sp.interpolate.interp1d(
        yspace, J_vals, kind="cubic", fill_value="extrapolate"
    )

    th_vals = [theta(y, t_estimate, J_estimate) * 180 / (np.pi) for y in y_vals]
    print(th_vals[-1])
    plot_diagram_threshold(
        y_vals,
        th_vals,
        10,
        "y (m)",
        "θ (°)",
        f"Twist angle along wing span at load factor {load_factor}",
    )


if __name__ == "__main__":
    plot_deflection(CL_d, point_loads, distributed_loads, load_factor, dynp)
    plot_twist(CL_d, point_torques, load_factor, dynp)
    plt.show()
