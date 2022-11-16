import scipy as sp
from stiffness import *
import matplotlib.pyplot as plt
import numpy as np
#Functions M(x) and T(y) need to be imported from WP4.1

def dvdy(y):
    result = sp.integrate.quad(lambda x: -M(x)/(MAT["E"]*MOI(x)[1]),0,y)
    return result[0]

def v(y):
    result = sp.integrate.quad(dvdy,0,y)[0]
    return result[0]

x = np.linspace(0,WING["span"]/2,100)
y1 = v(x)
plt.plot(x,y1)
plt.show ()

def theta(y):
    result = sp.integrate.quad(lambda x: T(x)/(MAT["G"]*torsional_constant(x)),0,y)[0]
    return result[0]

y2 = theta(x)
plt.plot(x,y2)
plt.show ()