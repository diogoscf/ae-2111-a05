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

# Centroid coordinates at a position y/(b/2) along the span (from wing root), using parameters in WINGBOX
# Coordinates given with (0,0) at leading edge
def centroid(y):
    chord = chord_y(y)
    centroids = [] # list of (x,y,A)
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
    # Spars
    for spar_pos in spars:
        h, y, *rest = airfoil_info(spar_pos)
        centroids.append([spar_pos*chord, y*chord, h*chord*spar_pos])

    # Skin Pieces
    for i in range(len(spars) - 1):
        start, end = spars[i], spars[i+1]
        y_start, y_end = airfoil_info(start)[2:], airfoil_info(end)[2:]
        x = (start+end)/2

        y_u = (y_start[0] + y_end[0])/2
        l_u = np.sqrt((end - start)**2 + (y_start[0] - y_end[0])**2)
        centroids.append([x*chord, y_u*chord, l_u*chord*WINGBOX["skin_thickness"]])

        y_l = (y_start[1] + y_end[1])/2
        l_l = np.sqrt((end - start)**2 + (y_start[1] - y_end[1])**2)
        centroids.append([x*chord, y_l*chord, l_l*chord*WINGBOX["skin_thickness"]])

    # Stringers
    for stringer in WINGBOX["stringers_top"]:
        l_spar_idx = bisect.bisect_left(spars, stringer) - 1
        #print(spars, stringer, l_spar_idx)
        l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
        y = np.interp(stringer, (l_spar, airfoil_info(l_spar)[2]), (r_spar, airfoil_info(r_spar)[2]))
        centroids.append([stringer*chord, y*chord, WINGBOX["stringer_area"]])

    for stringer in WINGBOX["stringers_bottom"]:
        l_spar_idx = bisect.bisect_left(spars, stringer) - 1
        l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
        y = np.interp(stringer, (l_spar, airfoil_info(l_spar)[3]), (r_spar, airfoil_info(r_spar)[3]))
        centroids.append([stringer*chord, y*chord, WINGBOX["stringer_area"]])

    centroids = np.array(centroids)
    c_x = np.sum(centroids[:,0]*centroids[:,2]) / np.sum(centroids[:,2])
    c_y = np.sum(centroids[:,1]*centroids[:,2]) / np.sum(centroids[:,2])

    return c_x, c_y

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
        """
        start, end = spars[0], spars[1]
        y_start, y_end = airfoil_info(start)[2:], airfoil_info(end)[2:]
        hl, hr = airfoil_info(start)[0]*chord, airfoil_info(end)[0]*chord
        lu = np.sqrt((end - start)**2 + (y_start[0] - y_end[0])**2)*chord
        ll = np.sqrt((end - start)**2 + (y_start[1] - y_end[1])**2)*chord
        J = 4*(areas[0]**2) / (((hl+hr)/(WINGBOX["spar_thickness"])) + ((ll+lu)/(WINGBOX["skin_thickness"]))])))
        """
        front_spar = [spars[0], airfoil_info(spars[0])[0], *airfoil_info(spars[0])[2:]]
        rear_spar = [spars[1], airfoil_info(spars[1])[0], *airfoil_info(spars[1])[2:]]
        front_spar_h = front_spar[1]*chord
        rear_spar_h = rear_spar[1]*chord
        x_skin = abs((rear_spar[0] - front_spar[0]))*chord

        y_skin_top = abs((front_spar[2] - rear_spar[2]))*chord     
        l_skin_top = np.sqrt(y_skin_top**2 + x_skin**2)

        y_skin_bottom = abs((front_spar[3] - rear_spar[3]))*chord
        l_skin_bottom = np.sqrt(y_skin_bottom**2+x_skin**2)
        
        i = ((front_spar_h + rear_spar_h)/WINGBOX["spar_thickness"]) + ((l_skin_bottom + l_skin_top)/WINGBOX["skin_thickness"])
        J = (4*(areas[0]**2))/i
        return J
    
    ncells = len(spars) - 1
    matrix = np.zeros((ncells+1, ncells+1))
    RHS = np.zeros(ncells+1)
    matrix[-1,:] = np.append(2*areas, [0])
    RHS[-1] = 1
    for i in range(ncells):
        start, end = spars[i], spars[i+1]
        y_start, y_end = airfoil_info(start)[2:], airfoil_info(end)[2:]
        hl, hr = airfoil_info(start)[0]*chord, airfoil_info(end)[0]*chord
        lu = np.sqrt((end - start)**2 + (y_start[0] - y_end[0])**2)*chord
        ll = np.sqrt((end - start)**2 + (y_start[1] - y_end[1])**2)*chord

        matrix[i, i] = (1/(2*areas[i]))*(((hl+hr)/WINGBOX["spar_thickness"]) + ((lu+ll)/WINGBOX["skin_thickness"]))
        if not i == 0:
            matrix[i, i-1] = -1/(2*areas[i])*(hl/WINGBOX["spar_thickness"])
        if not i == ncells - 1:
            matrix[i, i+1] = -1/(2*areas[i])*(hr/WINGBOX["spar_thickness"])
        
        matrix[i,-1] = -1
    
    solution = np.linalg.solve(matrix,RHS)
    J = 1/solution[-1]
    return J

#print(torsional_constant(0))

#Moment of inertia at a position y/(b/2) along the span
def MOI(y):
    chord = ((WING["taper_ratio"] - 1)*abs(y) + 1) * WING["root_chord"]
    spar_position = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
    centroid_y = centroid(y)
    Ixx = 0
    Iyy = 0

    #for top stringers
    for stringer in WINGBOX["stringers_top"]:
        l_spar_idx = bisect.bisect_left(spar_position, stringer) - 1
        l_spar, r_spar = spar_position[l_spar_idx], spar_position[l_spar_idx + 1]
        y_coord = np.interp(stringer, (l_spar, airfoil_info(l_spar)[2]), (r_spar, airfoil_info(r_spar)[2]))
        position = (chord * stringer,chord * y_coord)                                            #coordinates converted to meters 
        rel_position = (position[0] - centroid_y[0],position[1] - centroid_y[1])    #relative position to centroid
        Ixx += WINGBOX["stringer_area"] * (rel_position[1]**2)
        Iyy += WINGBOX["stringer_area"] * (rel_position[0]**2)
    
    #for bottom stringers
    for stringer in WINGBOX["stringers_bottom"]:
        l_spar_idx = bisect.bisect_left(spar_position, stringer) - 1
        l_spar, r_spar = spar_position[l_spar_idx], spar_position[l_spar_idx + 1]
        y_coord = np.interp(stringer, (l_spar, airfoil_info(l_spar)[2]), (r_spar, airfoil_info(r_spar)[2]))
        position = (chord * stringer,chord * y_coord)                                            #coordinates converted to meters 
        rel_position = (position[0] - centroid_y[0],position[1] - centroid_y[1])    #relative position to centroid
        Ixx += WINGBOX["stringer_area"] * (rel_position[1]**2)
        Iyy += WINGBOX["stringer_area"] * (rel_position[0]**2)

    #for spars
    for x in spar_position:
        position = (chord * x, chord * airfoil_info(x)[1])                          #coordinates converted to meters 
        rel_position = (position[0] - centroid_y[0],position[1] - centroid_y[1])    #relative position to centroid
        a = WINGBOX["spar_thickness"]
        b = airfoil_info(x)[0]
        Ixx += a*(b**3)/12 + a*b*(rel_position[1]**2)
        Iyy += (a**3)*b/12 + a*b*(rel_position[0]**2)

    #for skin
    for i in range(len(spar_position)-1):
        left_spar = spar_position[i]
        right_spar = spar_position[i+1]

        t = WINGBOX["skin_thickness"]

        #top element
        center = ( (left_spar + right_spar)/2 , (airfoil_info(left_spar)[2] + airfoil_info(right_spar)[2])/2 )                              #center of skin element                              
        theta = np.arctan((airfoil_info(left_spar)[2] - airfoil_info(right_spar)[2])/(left_spar - right_spar))                              #angle to x-axis
        position = (chord * center[0], chord * center[1]) # coordinates converted to meters
        rel_position = (position[0] - centroid_y[0],position[1] - centroid_y[1])                                                            #relative position to centroid
        w = np.sqrt((left_spar - right_spar)**2 + (airfoil_info(left_spar)[2] - airfoil_info(right_spar)[2])**2)
        Ixx += (w**3)*t*np.sin(theta)**2/12 + w*t*(rel_position[1]**2)
        Iyy += (w**3)*t*np.sin(theta)**2/12 + w*t*(rel_position[0]**2)

        #bottom element
        center = ( (left_spar + right_spar)/2 , (airfoil_info(left_spar)[3] + airfoil_info(right_spar)[3])/2 )
        theta = np.arctan((airfoil_info(left_spar)[3] - airfoil_info(right_spar)[3])/(left_spar - right_spar))
        position = (chord * center[0], chord * center[1])
        rel_position = (position[0] - centroid_y[0],position[1] - centroid_y[1])
        w = np.sqrt((left_spar - right_spar)**2 + (airfoil_info(left_spar)[3] - airfoil_info(right_spar)[3])**2)
        Ixx += (w**3)*t*np.sin(theta)**2/12 + w*t*(rel_position[1]**2)
        Iyy += (w**3)*t*np.sin(theta)**2/12 + w*t*(rel_position[0]**2)
    
    return Ixx, Iyy

print(centroid(1)[0]/chord_y(1), centroid(1)[1]/chord_y(1))