import scipy as sp
import matplotlib.pyplot as plt
import numpy as np

import stiffness
from params import *
from Diagrams import moment_calc, torque_calc
#Functions M(x) and T(y) need to be imported from WP4.1

rel = lambda y: y/(WING["span"]/2)

CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
ptloads = CRIT["point_loads"]
points = 300

y_vals = np.linspace(0, WING["span"]/2, points)
m_vals = moment_calc(CL_d, ptloads, load_factor, y_vals)
m_estimate = sp.interpolate.interp1d(y_vals,m_vals,kind="cubic",fill_value="extrapolate")
t_vals = torque_calc(CL_d, ptloads, load_factor, y_vals)
t_estimate = sp.interpolate.interp1d(y_vals,t_vals,kind="cubic",fill_value="extrapolate")

def M(y):
    return m_estimate(y)

def T(y):
    return t_estimate(y)

Ixx_vals = np.array([stiffness.MOI(rel(y))[0] for y in y_vals])
Ixx_estimate = sp.interpolate.interp1d(y_vals,Ixx_vals,kind="cubic",fill_value="extrapolate")

print(Ixx_vals)

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

def plot_diagram(x_vals, y_vals, xlab, ylab, plottitle):
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.set(xlabel=xlab, ylabel=ylab, title=plottitle)
    ax.grid()

def theta(y):
    result, _ = sp.integrate.quad(lambda x: T(x)/(MAT["G"]*torsional_constant(x)),0,y)
    return result


if __name__ == "__main__":
    v_vals = [v(y) for y in y_vals]
    plot_diagram(y_vals, v_vals, "y (m)", "v (m)", "Deflection along wing span")

    th_vals = [theta(y)*180/(np.pi) for y in y_vals]
    plot_diagram(y_vals, th_vals, "y (m)", "θ (°)", "Twist angle along wing span")

    plt.show()