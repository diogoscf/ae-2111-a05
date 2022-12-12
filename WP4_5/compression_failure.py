import sys
import os

from params import *
from stiffness import *
from diagrams import moment_calc
from deflections import *
import matplotlib.pyplot as plt



y = 0
spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])    
CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
point_loads = CRIT["point_loads"]
point_torques = CRIT["point_torques"]
distributed_loads = CRIT["distributed_loads"]
dynp = CRIT["dynp"]
points = 300
y_vals = np.linspace(0, WING["span"] / 2, points)
halfspan = WING["span"] / 2
sigma_yield = 276e6
yspace=y_vals
M_lst = moment_calc(CL_d, point_loads, distributed_loads, load_factor, dynp, yspace)
def stringer_c(h,w,t):
    y_bar = (h/2*h*t + w*t*t/2)/((w+h)*t)
    return y_bar



def MOI(y):
    stringers_top, stringers_bottom = stringers(y)
    chord = ((WING["taper_ratio"] - 1)*abs(y) + 1) * WING["root_chord"]
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
    centroid_y = centroid(y, stringers_top, stringers_bottom)
    Ixx = 0
    Izz = 0

    # for top stringers
    for stringer in stringers_top:
        l_spar_idx = bisect.bisect_left(spars, stringer) - 1
        l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
        z_coord = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[2], airfoil_info(r_spar)[2]))
        position = (chord * stringer, chord * z_coord) # coordinates converted to meters 
        rel_position = (position[0] - centroid_y[0], position[1] - centroid_y[1]) # relative position to centroid
       
       
        h = (5*WINGBOX["stringer_area"])**0.5
        w=h
        t = w/10 #meter
        Ixx += WINGBOX["stringer_area"] * ((rel_position[1]-(stringer_c(h,w,t)))**2) + (t*h**3)/12
        Izz += WINGBOX["stringer_area"] * (rel_position[0]**2)
    
    # for bottom stringers
    for stringer in stringers_bottom:
        l_spar_idx = bisect.bisect_left(spars, stringer) - 1
        l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
        z_coord = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[3], airfoil_info(r_spar)[3]))
        position = (chord * stringer, chord * z_coord) # coordinates converted to meters 
        rel_position = (position[0] - centroid_y[0], position[1] - centroid_y[1]) # relative position to centroid
        t = 0.005 #meter
        w= 0.05
        h = 0.05
        Ixx += WINGBOX["stringer_area"] * ((rel_position[1]-(stringer_c(h,w,t)))**2) + (t*h**3)/12
        Izz += WINGBOX["stringer_area"] * (rel_position[0]**2)
        #print(stringer, l_spar, r_spar, rel_position)

    # for spars
    for x in spars:
        position = (chord * x, chord * airfoil_info(x)[1]) # coordinates converted to meters 
        rel_position = (position[0] - centroid_y[0], position[1] - centroid_y[1]) # relative position to centroid
        t = thickness_y(y, *WINGBOX["spar_thickness"])
        h = airfoil_info(x)[0] * chord
        Ixx += t*(h**3)/12 + t*h*(rel_position[1]**2)
        Izz += (t**3)*h/12 + t*h*(rel_position[0]**2)

    # for skin
    for i in range(len(spars)-1):
        left_spar = spars[i]
        right_spar = spars[i+1]
        t = WINGBOX["skin_thickness"]

        # top element
        center = ((left_spar + right_spar)/2 , (airfoil_info(left_spar)[2] + airfoil_info(right_spar)[2])/2)                              #center of skin element                              
        theta = np.arctan((airfoil_info(right_spar)[2] - airfoil_info(left_spar)[2])/(right_spar - left_spar))                              #angle to x-axis
        position = (chord * center[0], chord * center[1]) # coordinates converted to meters
        rel_position = (position[0] - centroid_y[0], position[1] - centroid_y[1])                                                            #relative position to centroid
        w = (np.sqrt((left_spar - right_spar)**2 + (airfoil_info(left_spar)[2] - airfoil_info(right_spar)[2])**2))*chord
        Ixx += (w**3)*t*(np.sin(theta)**2)/12 + w*t*(rel_position[1]**2)
        Izz += (w**3)*t*(np.cos(theta)**2)/12 + w*t*(rel_position[0]**2)

        # bottom element
        center = ((left_spar + right_spar)/2 , (airfoil_info(left_spar)[3] + airfoil_info(right_spar)[3])/2)
        theta = np.arctan((airfoil_info(right_spar)[3] - airfoil_info(left_spar)[3])/(right_spar - left_spar))
        position = (chord * center[0], chord * center[1])
        rel_position = (position[0] - centroid_y[0], position[1] - centroid_y[1])
        w = (np.sqrt((left_spar - right_spar)**2 + (airfoil_info(left_spar)[3] - airfoil_info(right_spar)[3])**2))*chord
        Ixx += (w**3)*t*(np.sin(theta)**2)/12 + w*t*(rel_position[1]**2)
        Izz += (w**3)*t*(np.cos(theta)**2)/12 + w*t*(rel_position[0]**2)
    
    return Ixx, Izz

def area(y):
    chord_y = lambda y: (((WING["taper_ratio"] - 1) / (halfspan)) * abs(y) + 1) * WING["root_chord"] 
    chord = chord_y(y)
    area_spars = 0
    i=0
    t = thickness_y(y, *WINGBOX["spar_thickness"])
    area_skin = chord * 0.45 * 2 * WINGBOX["skin_thickness"]
    while i <= len(spars)-1:
        area_spars += airfoil_info(spars[i])[0]*chord*t
        i+=1
    area_stringers = WINGBOX["stringer_area"]*(len(stringers(y)[0])+len(stringers(y)[1]))
    return area_skin+area_stringers+area_spars

def sigma_y(y, yspace=y_vals): 
    chord_y = lambda y: (((WING["taper_ratio"] - 1) / (halfspan)) * abs(y) + 1) * WING["root_chord"] 
    z = chord_y(y/halfspan) * 0.0796/2
    if y == 0:
        M = M_lst[0]
    else:
        M = M_lst[int(round(y*halfspan*300/(WING["span"]/2),0))-1]
    sigma_y = M*z/MOI(y/halfspan)[0]
    if y <=0.35:
        sigma_y+= 180000/area(y)
    return sigma_y

def mos(y):
    mos = sigma_yield/abs(sigma_y(y))
    return mos

def sigma_y_plot():
    y=0
    i=0
    a=0
    sigma_y_lst=[]
    y_lst=[]
    while i <=150 and a<=1:
        a= sigma_y(y)
        i+=1
        sigma_y_lst.append(a)
        y_lst.append(y*halfspan)
        y+=1/300
    plt.plot(y_lst,sigma_y_lst)
    plt.show()
    
def mos_plot():
    y=0
    i=0
    a=0
    mos_lst=[]
    y_lst=[]
    while i <=150 and a<=1:
        a= mos(y)
        i+=1
        mos_lst.append(a)
        y_lst.append(y*halfspan)
        y+=1/300
    plt.plot(y_lst,mos_lst)
    plt.show()

def sigma_y_tension(y, yspace=y_vals): 
    chord_y = lambda y: (((WING["taper_ratio"] - 1) / (halfspan)) * abs(y) + 1) * WING["root_chord"] 
    z = chord_y(y/halfspan) * 0.0796/2
    if y == 0:
        M = M_lst[0]
    else:
        M = M_lst[int(round(y*halfspan*300/(WING["span"]/2),0))-1]
    sigma_y = M*-z/MOI(y/halfspan)[0]
    if y <=0.35:
        sigma_y-= 180000/area(y)
    return sigma_y

def mos_tension(y):
    mos = sigma_yield/abs(sigma_y_tension(y))
    return mos

def mos_plot_tension():
    y=0
    i=0
    a=0
    mos_lst=[]
    y_lst=[]
    while i <=150 and a<=1:
        a= mos_tension(y)
        i+=1
        mos_lst.append(a)
        y_lst.append(y*halfspan)
        y+=1/300
    plt.plot(y_lst,mos_lst)
    
def sigma_y_plot_tension():
    y=0
    i=0
    a=0
    sigma_y_lst=[]
    y_lst=[]
    while i <=150 and a<=1:
        a= sigma_y_tension(y)
        i+=1
        sigma_y_lst.append(a)
        y_lst.append(y*halfspan)
        y+=1/300
    plt.plot(y_lst,sigma_y_lst)
    plt.show()