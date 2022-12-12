import numpy as np
import scipy as sp
from scipy import integrate
from scipy import interpolate
import matplotlib.pyplot as plt
from math import pi
import stiffness
import distributions 
import diagrams
from params import *


def torque_calc(cl_d, point_loads=[], load_factor=1, dyn_p=10000, y_pos=diagrams.y_space):
    t_tab = []
    normal = distributions.N_prime(cl_d, (0.028 + cl_d**2 / (pi * 10 * 0.51)), y_pos, dyn_p)
    cm_function = distributions.M_prime(distributions.CM_at_AOA(distributions.AOA_specific_flight_regime(cl_d)), y_pos, dyn_p)
    intpl_cm = sp.interpolate.interp1d(y_pos, cm_function , kind="cubic", fill_value="extrapolate")
    intpl = sp.interpolate.interp1d(y_pos, normal, kind="cubic", fill_value="extrapolate")
    function = lambda y: intpl(y) * diagrams.distance_flexural_axis(y) + intpl_cm(y)
    for y in y_pos:
        estimate_t, _ = sp.integrate.quad(function, y, y_pos[-1])
        estimate_t *= load_factor
        for load, pos in point_loads:
            if y <= pos:
                estimate_t += load
        t_tab.append(estimate_t)
    return t_tab



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

print(multicell_shear_stress(0))

shear_torque_lst = []
torque = torque_calc(2.27,[],-1.5,1481)
for i in range(290, 300):
    shear_torque = list(multicell_shear_stress(i/299)*torque[i])
    shear_torque_lst.append(shear_torque)
print(shear_torque_lst)


