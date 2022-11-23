import scipy as sp
import matplotlib.pyplot as plt
import numpy as np

import stiffness
from params import *
from Diagrams import moment_calc, torque_calc
#Functions M(x) and T(y) need to be imported from WP4.1

rel = lambda y: y/(WING["span"]/2)

CL_d = 1
points = 100

y_vals = np.linspace(0, WING["span"]/2, points)
m_vals = moment_calc(CL_d, [], y_vals)
m_estimate = sp.interpolate.interp1d(y_vals,m_vals,kind="cubic",fill_value="extrapolate")
t_vals = torque_calc(CL_d, [], y_vals)
t_estimate = sp.interpolate.interp1d(y_vals,t_vals,kind="cubic",fill_value="extrapolate")

def M(y):
    return m_estimate(y)

def T(y):
    return t_estimate(y)

Iyy_vals = np.array([stiffness.MOI(rel(y))[1] for y in y_vals])
Iyy_estimate = sp.interpolate.interp1d(y_vals,Iyy_vals,kind="cubic",fill_value="extrapolate")

J_vals = np.array([stiffness.torsional_constant(rel(y)) for y in y_vals])
J_estimate = sp.interpolate.interp1d(y_vals,J_vals,kind="cubic",fill_value="extrapolate")

def MOI(y):
    return Iyy_estimate(y)

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

y1 = [v(x) for x in y_vals]
plt.plot(y_vals,y1)
plt.show()

def theta(y):
    result, _ = sp.integrate.quad(lambda x: T(x)/(MAT["G"]*torsional_constant(x)),0,y)
    return result

y2 = [theta(y) for y in y_vals]
plt.plot(y_vals,y2)
plt.show()