import matplotlib.pyplot as plt
import numpy as np

import stiffness
from params import *

def plot_diagram(x_vals, y_vals, xlab, ylab, plottitle):
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.set(xlabel=xlab, ylabel=ylab, title=plottitle)
    ax.grid()
    #plt.show()

y_vals = np.linspace(0,1,300)

moi = np.array([stiffness.MOI(y, WINGBOX) for y in y_vals])
plot_diagram(y_vals*stiffness.WING["span"]/2, moi[:,0], "y (m)", "$I_{xx}$ (m$^4$)", "Moment of Inertia (x-axis) along wing span")
plot_diagram(y_vals*stiffness.WING["span"]/2, moi[:,1], "y (m)", "$I_{zz}$ (m$^4$)", "Moment of Inertia (z-axis) along wing span")

J = np.array([stiffness.torsional_constant(y, WINGBOX) for y in y_vals])
plot_diagram(y_vals*stiffness.WING["span"]/2, J, "y (m)", "J (m$^4$)", "Torsional Constant along wing span")
"""
c = np.array([stiffness.centroid(y) for y in y_vals])
plot_diagram(y_vals*stiffness.WING["span"]/2, c[:,0], "y (m)", "Cx (m)", "Centroid Coordinate (x) along wing span")
plot_diagram(y_vals*stiffness.WING["span"]/2, c[:,1], "y (m)", "Cz (m)", "Centroid Coordinate (z) along wing span")
"""
plt.show()

#print(stiffness.centroid(y_space))