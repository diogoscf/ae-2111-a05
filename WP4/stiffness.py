import scipy as sp
from scipy import interpolate
import numpy as np
import os
import bisect

# Parametric Description of Wingbox
WINGBOX = {
    "front_spar": 0.2,
    "rear_spar": 0.8,
    "other_spars": [(0.5, 0.7)], # (x/c position value, y/(b/2) value of end of spar)
    "spar_thickness": 0.02, # meter
    "skin_thickness": 0.01, # meter
    "stringer_area": 0.003, # square meter
    "stringers_top": [0.3,0.4,0.5,0.7],
    "stringers_bottom": [0.3,0.4,0.5,0.7]
}

# Wing Parametric Description (values in SI)
WING = {
    "span": 43.58, # meter
    "root_chord": 6.86, # meter
    "taper_ratio": 0.27
}

airfoil_file_path = os.path.join(os.path.dirname(__file__), "../KC-135 Winglet.dat")
airfoil_data = np.genfromtxt(airfoil_file_path) # airfoil data points
#print(airfoil_data)

# Airfoil Info at a point x/c, returns thickness, camber, upper and lower values (normalised to chord)
def airfoil_info(x):
    upper = airfoil_data[0:(len(airfoil_data)-1)//2][::-1]
    lower = airfoil_data[(len(airfoil_data)-1)//2:len(airfoil_data)]
    heights = np.array([(upper[i][0], upper[i][1] - lower[i][1]) for i in range(len(upper))])
    cambers = np.array([(upper[i][0], (upper[i][1] + lower[i][1])/2) for i in range(len(upper))])
    h = sp.interpolate.interp1d(heights[:,0], heights[:,1],kind="linear")
    c = sp.interpolate.interp1d(cambers[:,0], cambers[:,1],kind="linear")
    u = sp.interpolate.interp1d(upper[:,0], upper[:,1],kind="linear")
    l = sp.interpolate.interp1d(lower[:,0], lower[:,1],kind="linear")
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

print(centroid(0))

# Returns a list of enclosed areas in the wingbox at y/(b/2) along span
def enclosed_areas(y):
    areas = []
    spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
    for i in range(len(spars) - 1):
        l_spar, r_spar = spars[i], spars[i+1]
        l_height, r_height = airfoil_info(l_spar)[0], airfoil_info(r_spar)[0]
        areas.append((chord_y(y)**2)*(r_spar - l_spar)*(l_height + r_height)/2)

    return areas
