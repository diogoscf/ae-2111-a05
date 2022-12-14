from params import *
import numpy as np
import matplotlib.pyplot as plt
import bisect

from stiffness import airfoil_info, airfoil_data, chord_y, centroid, stringers

wbox = WINGBOX

sweep = WING["LE_sweep"] * np.pi / 180
halfspan = WING["span"] / 2

spars = sorted([(wbox["front_spar"], 1), (wbox["rear_spar"], 1), *wbox["other_spars"]])

"""Unswept Wing"""

fig, ax = plt.subplots(figsize=(12, 6))

diff = (chord_y(0) - chord_y(1)) / 2

ax.plot((0, halfspan), (chord_y(0), chord_y(1) + diff), color="black") # Leading Edge
ax.plot((0, halfspan), (0, 0 + diff), color="black") # Trailing Edge

ax.plot((0, 0), (0, chord_y(0)), color="black") # Root Chord
ax.plot((halfspan, halfspan), (0 + diff, chord_y(1) + diff), color="black") # Tip Chord

for x, end in spars:
    loc_diff = (chord_y(0) - chord_y(end)) / 2
    ax.plot((0, end * halfspan), ((1 - x) * chord_y(0), (1 - x) * chord_y(end) + loc_diff), color="red") # Spars

ax.set(title="Spar Positions in Unswept Wing")
ax.axis("scaled")


"""Swept Wing"""

fig, ax = plt.subplots(figsize=(12, 6))

x_end_le = halfspan * np.tan(sweep)
ax.plot((0, halfspan), (chord_y(0), chord_y(0) - x_end_le), color="black") # Leading Edge
ax.plot((0, halfspan), (0, chord_y(0) - x_end_le - chord_y(1)), color="black") # Trailing Edge

ax.plot((0, 0), (0, chord_y(0)), color="black") # Root Chord
ax.plot((halfspan, halfspan), (chord_y(0) - x_end_le, chord_y(0) - x_end_le - chord_y(1)), color="black") # Tip Chord

for x, end in spars:
    loc_end_le = end * halfspan * np.tan(sweep)
    ax.plot((0, end * halfspan), ((1 - x) * chord_y(0), chord_y(0) - loc_end_le - (x*chord_y(end))), color="red") # Spars

ax.set(title="Spar Positions in Swept Wing")
ax.axis("scaled")


plt.xlim([0, (WING["span"]/2)*1.1])
plt.show()

