import matplotlib.pyplot as plt
import numpy as np

import stiffness

def plot_diagram(x_vals, y_vals, xlab, ylab, plottitle):
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    ax.set(xlabel=xlab, ylabel=ylab, title=plottitle)
    ax.grid()
    #plt.show()

y_vals = np.linspace(-1,1,1001)

moi = np.array([stiffness.MOI(y) for y in y_vals])
plot_diagram(y_vals*stiffness.WING["span"]/2, moi[:,0], "y (m)", "Ixx (m^4)", "Moment of Inertia (x-axis) along wing span")
plot_diagram(y_vals*stiffness.WING["span"]/2, moi[:,1], "y (m)", "Iyy (m^4)", "Moment of Inertia (y-axis) along wing span")

J = np.array([stiffness.torsional_constant(y) for y in y_vals])
plot_diagram(y_vals*stiffness.WING["span"]/2, J, "y (m)", "J", "Torsional Constant along wing span")

plt.show()

#print(stiffness.centroid(y_space))