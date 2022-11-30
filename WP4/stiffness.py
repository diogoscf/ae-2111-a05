import bisect
import os

import numpy as np
import scipy as sp
from scipy import interpolate

from params import *

airfoil_file_path = os.path.join(os.path.dirname(__file__), "../KC-135 Winglet.dat")
airfoil_data = np.genfromtxt(airfoil_file_path) # airfoil data points
#print(airfoil_data)

# Airfoil Info at a point x/c, returns thickness, camber, upper and lower values (normalised to chord)
def airfoil_info(x):
    upper = airfoil_data[0:(len(airfoil_data)-1)//2][::-1]
    lower = airfoil_data[(len(airfoil_data)-1)//2:len(airfoil_data)]
    heights = np.array([(upper[i][0], upper[i][1] - lower[i][1]) for i in range(len(upper))])
    cambers = np.array([(upper[i][0], (upper[i][1] + lower[i][1])/2) for i in range(len(upper))])
    h = sp.interpolate.interp1d(heights[:,0], heights[:,1],kind="linear")  # type: ignore
    c = sp.interpolate.interp1d(cambers[:,0], cambers[:,1],kind="linear")  # type: ignore
    u = sp.interpolate.interp1d(upper[:,0], upper[:,1],kind="linear")  # type: ignore
    l = sp.interpolate.interp1d(lower[:,0], lower[:,1],kind="linear")  # type: ignore
    return h(x), c(x), u(x), l(x)

steiner = lambda A, d: A*(d**2)
rect_MMOI = lambda b,h: b*(h**3)/12

chord_y = lambda y: ((WING["taper_ratio"] - 1)*abs(y) + 1) * WING["root_chord"]

def distribute_stringers(fspar, rspar, nstringers):
    stringers = []
    if nstringers == 0: return stringers
    dist = (rspar - fspar) / nstringers
    for i in range(nstringers):
        stringers.append(fspar + (i+(1/2))*dist)
    return stringers

def stringers(y):
    fspar, rspar = WINGBOX["front_spar"], WINGBOX["rear_spar"]
    nstringers_top, nstringers_bottom = 0, 0
    for n, loc in WINGBOX["stringers_top"]:
        if y <= loc:
            nstringers_top = n
            break
    for n, loc in WINGBOX["stringers_bottom"]:
        if y <= loc:
            nstringers_bottom = n
            break
    stringers_top = distribute_stringers(fspar, rspar, nstringers_top)
    stringers_bottom = distribute_stringers(fspar, rspar, nstringers_bottom)

    return stringers_top, stringers_bottom

# Centroid coordinates at a position y/(b/2) along the span (from wing root), using parameters in WINGBOX
# Coordinates given with (x,z) = (0,0) at leading edge (camber line)
def centroid(y, stringers_top=[], stringers_bottom=[]):
    chord = chord_y(y)
    centroids = [] # list of (x,z,A)
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
    # Spars
    for spar_pos in spars:
        h, z, *rest = airfoil_info(spar_pos)
        centroids.append([spar_pos*chord, z*chord, h*chord*WINGBOX["spar_thickness"]])

    # Skin Pieces
    for i in range(len(spars) - 1):
        start, end = spars[i], spars[i+1]
        z_start, z_end = airfoil_info(start)[2:], airfoil_info(end)[2:]
        x = (start+end)/2

        z_u = (z_start[0] + z_end[0])/2
        l_u = np.sqrt((end - start)**2 + (z_start[0] - z_end[0])**2)
        centroids.append([x*chord, z_u*chord, l_u*chord*WINGBOX["skin_thickness"]])

        z_l = (z_start[1] + z_end[1])/2
        l_l = np.sqrt((end - start)**2 + (z_start[1] - z_end[1])**2)
        centroids.append([x*chord, z_l*chord, l_l*chord*WINGBOX["skin_thickness"]])

    # Stringers
    for stringer in stringers_top:
        l_spar_idx = bisect.bisect_left(spars, stringer) - 1
        #print(spars, stringer, l_spar_idx)
        l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
        z = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[2], airfoil_info(r_spar)[2]))
        centroids.append([stringer*chord, z*chord, WINGBOX["stringer_area"]])

    for stringer in stringers_bottom:
        l_spar_idx = bisect.bisect_left(spars, stringer) - 1
        l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
        z = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[3], airfoil_info(r_spar)[3]))
        centroids.append([stringer*chord, z*chord, WINGBOX["stringer_area"]])

    centroids = np.array(centroids)
    c_x = np.sum(centroids[:,0]*centroids[:,2]) / np.sum(centroids[:,2])
    c_z = np.sum(centroids[:,1]*centroids[:,2]) / np.sum(centroids[:,2])

    return c_x, c_z

#print(centroid(0))

# Returns a list of enclosed areas in the wingbox at y/(b/2) along span
def enclosed_areas(y, spars):
    areas = []
    for i in range(len(spars) - 1):
        l_spar, r_spar = spars[i], spars[i+1]
        l_height, r_height = airfoil_info(l_spar)[0], airfoil_info(r_spar)[0]
        areas.append((chord_y(y)**2)*(r_spar - l_spar)*(l_height + r_height)/2)

    return areas

def torsional_constant(y):
    chord = chord_y(y)
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
    areas = np.array(enclosed_areas(y, spars))

    if len(spars) == 2:
        start, end = spars[0], spars[1]
        z_start, z_end = airfoil_info(start)[2:], airfoil_info(end)[2:]
        hl, hr = airfoil_info(start)[0]*chord, airfoil_info(end)[0]*chord
        lu = np.sqrt((end - start)**2 + (z_start[0] - z_end[0])**2)*chord
        ll = np.sqrt((end - start)**2 + (z_start[1] - z_end[1])**2)*chord
        J = 4*(areas[0]**2) / (((hl+hr)/(WINGBOX["spar_thickness"])) + ((ll+lu)/(WINGBOX["skin_thickness"])))
        return J
    
    ncells = len(spars) - 1
    matrix = np.zeros((ncells+1, ncells+1))
    RHS = np.zeros(ncells+1)
    matrix[-1,:] = np.append(2*areas, [0])
    RHS[-1] = 1
    for i in range(ncells):
        start, end = spars[i], spars[i+1]
        z_start, z_end = airfoil_info(start)[2:], airfoil_info(end)[2:]
        hl, hr = airfoil_info(start)[0]*chord, airfoil_info(end)[0]*chord
        lu = np.sqrt((end - start)**2 + (z_start[0] - z_end[0])**2)*chord
        ll = np.sqrt((end - start)**2 + (z_start[1] - z_end[1])**2)*chord

        matrix[i, i] = (1/(2*areas[i]))*(((hl+hr)/WINGBOX["spar_thickness"]) + ((lu+ll)/WINGBOX["skin_thickness"]))
        if not i == 0:
            matrix[i, i-1] = -1/(2*areas[i])*(hl/WINGBOX["spar_thickness"])
        if not i == ncells - 1:
            matrix[i, i+1] = -1/(2*areas[i])*(hr/WINGBOX["spar_thickness"])
        
        matrix[i,-1] = -1
    
    solution = np.linalg.solve(matrix,RHS)
    J = 1/solution[-1]
    return J

#print(torsional_constant(1))

#Moment of inertia at a position y/(b/2) along the span
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
        Ixx += WINGBOX["stringer_area"] * (rel_position[1]**2)
        Izz += WINGBOX["stringer_area"] * (rel_position[0]**2)
    
    # for bottom stringers
    for stringer in stringers_bottom:
        l_spar_idx = bisect.bisect_left(spars, stringer) - 1
        l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
        z_coord = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[3], airfoil_info(r_spar)[3]))
        position = (chord * stringer, chord * z_coord) # coordinates converted to meters 
        rel_position = (position[0] - centroid_y[0], position[1] - centroid_y[1]) # relative position to centroid
        Ixx += WINGBOX["stringer_area"] * (rel_position[1]**2)
        Izz += WINGBOX["stringer_area"] * (rel_position[0]**2)
        #print(stringer, l_spar, r_spar, rel_position)

    # for spars
    for x in spars:
        position = (chord * x, chord * airfoil_info(x)[1]) # coordinates converted to meters 
        rel_position = (position[0] - centroid_y[0], position[1] - centroid_y[1]) # relative position to centroid
        t = WINGBOX["spar_thickness"]
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

# print(centroid(1)[0]/chord_y(1), centroid(1)[1]/chord_y(1))
# print(MOI(1)[0]/MOI(0)[0])