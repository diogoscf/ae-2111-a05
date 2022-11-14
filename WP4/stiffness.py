import scipy as sp
from scipy import interpolate
import numpy as np

AIRFOIL_CHORD = 1 # Airfoil Chord Length [meters]

airfoil_data = np.genfromtxt("../KC-135 Winglet.dat") # airfoil data points
#print(airfoil_data)

# Airfoil Thickness at a point x (RELATIVE TO CHORD!)
def airfoil_thickness(x):
    upper = airfoil_data[0:(len(airfoil_data)-1)//2][::-1]
    lower = airfoil_data[(len(airfoil_data)-1)//2:len(airfoil_data)]
    heights = np.array([(upper[i][0], upper[i][1] - lower[i][1]) for i in range(len(upper))])

    f = sp.interpolate.interp1d(heights[:,0], heights[:,1],kind="linear")
    return f(x)
