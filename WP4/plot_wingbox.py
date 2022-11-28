from params import *
import numpy as np
import matplotlib.pyplot as plt
import bisect

from stiffness import airfoil_info, airfoil_data, chord_y

y = 0
chord = chord_y(y)

fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(airfoil_data[:,0]*chord, airfoil_data[:,1]*chord, color="black") # Airfoil

spars = sorted([WINGBOX["front_spar"], WINGBOX["rear_spar"], *[s[0] for s in WINGBOX["other_spars"] if s[1] >= abs(y)]])

for i, s in enumerate(spars):
    ax.plot((s*chord, s*chord), [airfoil_info(s)[2]*chord, airfoil_info(s)[3]*chord], color="red") # Spars
    if i < len(spars)-1:
        ax.plot((s*chord, spars[i+1]*chord), [airfoil_info(s)[2]*chord, airfoil_info(spars[i+1])[2]*chord], color="red") # Top Skin
        ax.plot((s*chord, spars[i+1]*chord), [airfoil_info(s)[3]*chord, airfoil_info(spars[i+1])[3]*chord], color="red") # Bottom Skin

for stringer in WINGBOX["stringers_top"]:
    l_spar_idx = bisect.bisect_left(spars, stringer) - 1
    l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
    z = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[2], airfoil_info(r_spar)[2]))
    ax.plot(stringer*chord, z*chord, marker="o", color="blue") # Top Stringers

for stringer in WINGBOX["stringers_bottom"]:
    l_spar_idx = bisect.bisect_left(spars, stringer) - 1
    l_spar, r_spar = spars[l_spar_idx], spars[l_spar_idx + 1]
    z = np.interp(stringer, (l_spar, r_spar), (airfoil_info(l_spar)[3], airfoil_info(r_spar)[3]))
    ax.plot(stringer*chord, z*chord, marker="o", color="blue") # Bottom Stringers

plt.xlim([0, chord])
plt.ylim([-chord/4, chord/4])
plt.show()

