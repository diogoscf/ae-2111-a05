from params import *
import numpy as np
import matplotlib.pyplot as plt

from stiffness import chord_y
import design_options

wbox = design_options.option_new_2

sweep = WING["LE_sweep"] * np.pi / 180
halfspan = WING["span"] / 2

spars = sorted([[wbox["front_spar"], 1], [wbox["rear_spar"], 1], *wbox["other_spars"]])

"""Unswept Wing"""

fig, ax = plt.subplots(figsize=(12, 6))

diff = (chord_y(0) - chord_y(1)) / 2

ax.plot((0, halfspan), (chord_y(0), chord_y(1) + diff), color="black") # Leading Edge
ax.plot((0, halfspan), (0, 0 + diff), color="black") # Trailing Edge

for x, end in spars:
    loc_diff = (chord_y(0) - chord_y(end)) / 2
    ax.plot((0, end * halfspan), ((1 - x) * chord_y(0), (1 - x) * chord_y(end) + loc_diff), color="red") # Spars

for r in wbox["ribs"]:
    loc_diff = (chord_y(0) - chord_y(r)) / 2
    ax.plot((r * halfspan, r * halfspan), (loc_diff, chord_y(r) + loc_diff), color="blue") # Ribs


ax.plot((0, 0), (0, chord_y(0)), color="blue") # Root Chord
ax.plot((halfspan, halfspan), (0 + diff, chord_y(1) + diff), color="blue") # Tip Chord

#ax.set(title="Spar and Rib Positions in Unswept Wing")
ax.axis("scaled")


"""Swept Wing"""

fig, ax = plt.subplots(figsize=(12, 6))

x_end_le = halfspan * np.tan(sweep)
ax.plot((0, halfspan), (chord_y(0), chord_y(0) - x_end_le), color="black") # Leading Edge
ax.plot((0, halfspan), (0, chord_y(0) - x_end_le - chord_y(1)), color="black") # Trailing Edge

for x, end in spars:
    loc_end_le = end * halfspan * np.tan(sweep)
    ax.plot((0, end * halfspan), ((1 - x) * chord_y(0), chord_y(0) - loc_end_le - (x*chord_y(end))), color="red") # Spars

for r in wbox["ribs"]:
    loc_end_le = r * halfspan * np.tan(sweep)
    ax.plot((r * halfspan, r * halfspan), (chord_y(0) - loc_end_le, chord_y(0) - loc_end_le - chord_y(r)), color="blue") # Ribs

ax.plot((0, 0), (0, chord_y(0)), color="blue") # Root Chord
ax.plot((halfspan, halfspan), (chord_y(0) - x_end_le, chord_y(0) - x_end_le - chord_y(1)), color="blue") # Tip Chord

#ax.set(title="Spar and Rib Positions in Swept Wing")
ax.axis("scaled")


plt.xlim([0, (WING["span"]/2)*1.1])
plt.show()

