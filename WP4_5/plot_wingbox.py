from params import *
import numpy as np
import matplotlib.pyplot as plt
import bisect

from stiffness import airfoil_info, airfoil_data, chord_y, centroid, stringers

y = 0
chord = chord_y(y)

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(airfoil_data[:,0]*chord, airfoil_data[:,1]*chord, color="black") # Airfoil

spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])
stringers_top, stringers_bottom = stringers(y, WINGBOX)

show_centroids = False

for i, s in enumerate(spars):
    ax.plot((s*chord, s*chord), [airfoil_info(s)[2]*chord, airfoil_info(s)[3]*chord], color="red") # Spars
    if show_centroids: ax.plot(chord * s, chord * airfoil_info(s)[1], marker="x", color="black")
    if i < len(spars)-1:
        ax.plot((s*chord, spars[i+1]*chord), [airfoil_info(s)[2]*chord, airfoil_info(spars[i+1])[2]*chord], color="red") # Top Skin
        if show_centroids: ax.plot(chord*(s + spars[i+1])/2 , chord*(airfoil_info(s)[2] + airfoil_info(spars[i+1])[2])/2, marker="x", color="black")
        ax.plot((s*chord, spars[i+1]*chord), [airfoil_info(s)[3]*chord, airfoil_info(spars[i+1])[3]*chord], color="red") # Bottom Skin
        if show_centroids: ax.plot(chord*(s + spars[i+1])/2 , chord*(airfoil_info(s)[3] + airfoil_info(spars[i+1])[3])/2, marker="x", color="black")

for stringer in stringers_top:
    l_spar_idx = bisect.bisect_left(spars, stringer) - 1
    l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
    z = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[2], airfoil_info(r_spar)[2]))
    ax.plot(stringer*chord, z*chord, marker=".", color="blue") # Top Stringers

for stringer in stringers_bottom:
    l_spar_idx = bisect.bisect_left(spars, stringer) - 1
    l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
    z = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[3], airfoil_info(r_spar)[3]))
    ax.plot(stringer*chord, z*chord, marker=".", color="blue") # Bottom Stringers


centroid_pos = centroid(y, stringers_top, stringers_bottom, WINGBOX)
ax.plot(centroid_pos[0], centroid_pos[1], marker="x", color="green") # Centroid
ax.plot(centroid_pos[0], centroid_pos[1]-0.05, marker="$C.G.$", color="green")

plt.xlim([0, chord])
plt.ylim([-chord/4, chord/4])
plt.show()

#print(MOI(y))

