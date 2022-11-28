import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import numpy as np

import stiffness
from params import *
from Diagrams import moment_calc, torque_calc
#Functions M(x) and T(y) need to be imported from WP4.1

rel = lambda y: y/(WING["span"]/2)

CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
ptloads = CRIT["point_loads"]
distloads = CRIT["distributed_loads"]
dynp = CRIT["dynp"]
points = 300

y_vals = np.linspace(0, WING["span"]/2, points)
m_vals = moment_calc(CL_d, ptloads, distloads, load_factor, dynp, y_vals)
m_estimate = sp.interpolate.interp1d(y_vals,m_vals,kind="cubic",fill_value="extrapolate")
t_vals = torque_calc(CL_d, ptloads, load_factor, dynp, y_vals)
t_estimate = sp.interpolate.interp1d(y_vals,t_vals,kind="cubic",fill_value="extrapolate")

def M(y):
    return m_estimate(y)

def T(y):
    return t_estimate(y)

Ixx_vals = np.array([stiffness.MOI(rel(y))[0] for y in y_vals])
Ixx_estimate = sp.interpolate.interp1d(y_vals,Ixx_vals,kind="cubic",fill_value="extrapolate")

#print(Ixx_vals)

J_vals = np.array([stiffness.torsional_constant(rel(y)) for y in y_vals])
J_estimate = sp.interpolate.interp1d(y_vals,J_vals,kind="cubic",fill_value="extrapolate")

def MOI(y):
    return Ixx_estimate(y)

def torsional_constant(y):
    return J_estimate(y)

def dvdy(y):
    result, _ = sp.integrate.quad(lambda x: -M(x)/(MAT["E"]*MOI(x)),0,y)
    return result

dv_vals = np.array([dvdy(y) for y in y_vals])
dv_estimate = sp.interpolate.interp1d(y_vals,dv_vals,kind="cubic",fill_value="extrapolate")

def v(y):
    result, _ = sp.integrate.quad(dv_estimate,0,y)
    return result

def plot_diagram_threshold(x_vals, y_vals, maxval, xlab, ylab, plottitle):
    fig, ax = plt.subplots()

    cmap = ListedColormap(["blue", "red"])
    norm = BoundaryNorm([np.min(y_vals), maxval, np.max(y_vals)], cmap.N)

    points = np.array([x_vals, y_vals]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(y_vals)

    ax.add_collection(lc)
    ax.set_xlim(np.min(x_vals), np.max(x_vals))
    ax.set_ylim(np.min(y_vals)*1.1, np.max(y_vals)*1.1)

    ax.set(xlabel=xlab, ylabel=ylab, title=plottitle)
    ax.grid()
    ax.axhline(maxval, color='k', ls='--')

def theta(y):
    result, _ = sp.integrate.quad(lambda x: T(x)/(MAT["G"]*torsional_constant(x)),0,y)
    return result


if __name__ == "__main__":
    v_vals = [v(y) for y in y_vals]
    plot_diagram_threshold(y_vals, v_vals, 0.15*WING["span"], "y (m)", "v (m)", "Deflection along wing span")

    th_vals = [theta(y)*180/(np.pi) for y in y_vals]
    plot_diagram_threshold(y_vals, th_vals, 15, "y (m)", "θ (°)", "Twist angle along wing span")

    plt.show()