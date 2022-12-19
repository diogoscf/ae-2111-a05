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



def multicell_shear_stress(y, wbox = WINGBOX):
    chord = stiffness.chord_y(y)
    t_spar = stiffness.thickness_y(y, *wbox["spar_thickness"])
    t_skin = wbox["skin_thickness"]
    spars = sorted([wbox["front_spar"], wbox["rear_spar"], *[s[0] for s in wbox["other_spars"] if s[1] >= abs(y)]])
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


#print(multicell_shear_stress(2/299)*torque_calc(2.27,[],-1.5,1481)[2])


def shear_torque_stress_calc(cl_d, point_loads=[], load_factor=1, dyn_p=10000, y_pos=diagrams.y_space):
    shear_torque_lst = []
    torque = torque_calc(cl_d, point_loads, load_factor, dyn_p, y_pos)
    for i in range(0,300):
        shear_torque = list(multicell_shear_stress(i/299)*torque[i])
        shear_torque_lst.append(shear_torque)
    return shear_torque_lst

def shear_stress_calc(cl_d, point_loads=[], distributed_loads=[], load_factor=1, dyn_p=10000, y_pos=diagrams.y_space):
    tr = WINGBOX["spar_thickness"][0]
    tt = WINGBOX["spar_thickness"][1]
    shear_lst = []
    shear = diagrams.shear_force_calc(cl_d, point_loads, distributed_loads, load_factor, dyn_p, y_pos)
    for i in range(0,300):
        thickness = stiffness.thickness_y(i/299, tr, tt)
        chord = stiffness.chord_y(i/299)
        spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(i/299)]])
        heights = []
        for spar in spars:
            heights.append(chord*stiffness.airfoil_info(spar)[0])
        sum_heights = sum(heights)
        avg_height = sum_heights/len(heights)
        tau_avg = shear[i]/(thickness*sum_heights)
        shear_section = []
        for j in range(len(spars)):
            k_v = 3/2*(heights[j]/avg_height)**2
            tau_max = k_v * tau_avg
            shear_section.append(tau_max)
        shear_lst.append(shear_section)
    return shear_lst 

def total_stress_calc(cl_d, point_loads=[], distributed_loads=[], load_factor=1, dyn_p=10000, y_pos=diagrams.y_space):
    torque = shear_torque_stress_calc(cl_d, point_loads, load_factor, dyn_p, y_pos)
    shear = shear_stress_calc(cl_d, point_loads, distributed_loads, load_factor, dyn_p, y_pos)
    stress_list = []
    for i in range(300):
        spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(i/299)]])
        spar_num = len(spars)
        stresses = []
        stresses.append(shear[i][0]-torque[i][0])
        if spar_num >= 3:
            for j in range(1,spar_num-1):
                stresses.append(shear[i][j]+torque[i][j-1]-torque[i][j])
        stresses.append(shear[i][spar_num-1]+torque[i][spar_num-2])
        stress_list.append(stresses)
    return stress_list

def critical_shear_stress():
    stress_list = []
    k_s=9
    v=1/3
    for i in range(0,300):
        thickness = stiffness.thickness_y(i/299, *WINGBOX["spar_thickness"])
        chord = stiffness.chord_y(i/299)
        spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(i/299)]])
        heights = []
        for spar in spars:
            heights.append(chord*stiffness.airfoil_info(spar)[0])
        stresses = []
        for j in range(len(spars)):
            crit_stress = pi**2*k_s*MAT['E']/(12*(1-v**2))*(thickness/heights[j])**2
            stresses.append(crit_stress)
        stress_list.append(stresses)
    return stress_list

print(critical_shear_stress()[0])

print(total_stress_calc(0.9,[], [], 3.75 ,8328)[0])

def margin_safety(cl_d, point_loads=[], distributed_loads=[], load_factor=1, dyn_p=10000, y_pos=diagrams.y_space):
    margin_safety_list=[]
    critical = critical_shear_stress()
    total = total_stress_calc(cl_d, point_loads, distributed_loads, load_factor, dyn_p, y_pos)
    for i in range(300):
        margin_per_spar = []
        spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(i/299)]])
        for j in range(len(spars)):
            margin = critical[i][j]/total[i][j]
            margin_per_spar.append(margin)
        margin_safety_list.append(margin_per_spar)
    return margin_safety_list

#def margin_of_safety_plot(spar):
    #margin_of_safety = margin_of_safety(cl_d, point_loads, distributed_loads, load_factor, dyn_p, y_pos)
    #y = margin_of_safety[spar]
    #x = diagrams.y_space


                    
            

