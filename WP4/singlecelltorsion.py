import numpy as np
import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
from math import pi
import stiffness
import Distributions 
import Diagrams 

from params import *


def multicell_shear_stress(y):
    chord = stiffness.chord_y(y)
    t_spar = stiffness.thickness_y(y, *WINGBOX["spar_thickness"])
    t_skin = WINGBOX["skin_thickness"]
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
    areas = np.array(stiffness.enclosed_areas(y, spars))

    if len(spars) == 2:
        start, end = spars[0], spars[1]
        z_start, z_end = stiffness.airfoil_info(start)[2:], stiffness.airfoil_info(end)[2:]
        hl, hr = stiffness.airfoil_info(start)[0]*chord, stiffness.airfoil_info(end)[0]*chord
        lu = np.sqrt((end - start)**2 + (z_start[0] - z_end[0])**2)*chord
        ll = np.sqrt((end - start)**2 + (z_start[1] - z_end[1])**2)*chord
        J = 4*(areas[0]**2) / (((hl+hr)/(t_spar)) + ((ll+lu)/(t_skin)))
        return J
    
    ncells = len(spars) - 1
    matrix = np.zeros((ncells+1, ncells+1))
    RHS = np.zeros(ncells+1)
    matrix[-1,:] = np.append(2*areas, [0])
    RHS[-1] = 1
    for i in range(ncells):
        start, end = spars[i], spars[i+1]
        z_start, z_end = stiffness.airfoil_info(start)[2:], stiffness.airfoil_info(end)[2:]
        hl, hr = stiffness.airfoil_info(start)[0]*chord, stiffness.airfoil_info(end)[0]*chord
        lu = np.sqrt((end - start)**2 + (z_start[0] - z_end[0])**2)*chord
        ll = np.sqrt((end - start)**2 + (z_start[1] - z_end[1])**2)*chord

        matrix[i, i] = (1/(2*areas[i]))*(((hl+hr)/t_spar) + ((lu+ll)/t_skin))
        if not i == 0:
            matrix[i, i-1] = -1/(2*areas[i])*(hl/t_spar)
        if not i == ncells - 1:
            matrix[i, i+1] = -1/(2*areas[i])*(hr/t_spar)
        
        matrix[i,-1] = -1
    solution = np.linalg.solve(matrix,RHS)
    shear_stress = solution/t_spar
    return shear_stress[0:-1]

print(multicell_shear_stress(1))

