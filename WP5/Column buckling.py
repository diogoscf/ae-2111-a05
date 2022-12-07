import numpy as np
import matplotlib.pyplot as plt

#numbers below are arbitrary
STRINGER = {
    "vertical_l": 100, #mm
    "horizontal_l": 100, #mm
    "thickness": 5, #mm
    "number": [60,40,20],
    "area_(wanted)": 480, #mm^2
}

#code for producing moment of inertia vs thickness
'''
vertical_l = L
horizontal_l = b
thickness = t
number = N
area_(wanted) = A
'''

#calculation in mm
def MOI(t,A):
    t = float(t)
    A = float(A)
    b = 10*t
    L = (10*A/b)-b
    MOI_ind = (b*t*(L**2/(0.5*(L+b)))**2) + (0.5*t*L**3) + (L**2*t/2)+(L*t/4*((L**2)/(L+b))**2) + ((b*t + L*t)*(0.5*(L**2 + b*t)/(L+b))**2)
    return MOI_ind

xtab = []
y1tab = []
for t in np.arange(0.1,20,0.2):
    xtab.append(t)
    y1 = MOI(t,4.8) #Assumed the total area is 480 [mm] and 100 stringer is used so the individual stringer's area is 4.8
    y1tab.append(y1)

plt.plot(xtab,y1tab)
plt.show()
print(y1tab)
