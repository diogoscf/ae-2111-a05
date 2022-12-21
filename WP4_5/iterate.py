import numpy as np
import scipy as sp
from scipy import interpolate

from params import *
import design_options
from stresses import sigma_y
from diagrams import moment_calc
from stiffness import MOI

rel = lambda y: y / (WING["span"] / 2)

CL_d = CRIT["cld"]
load_factor = CRIT["load_factor"]
point_loads = CRIT["point_loads"]
point_torques = CRIT["point_torques"]
distributed_loads = CRIT["distributed_loads"]
dynp = CRIT["dynp"]
points = 300
halfspan = WING["span"] / 2
y_vals = np.linspace(0, halfspan, points)

def maxstress(wbox):
    M = moment_calc(CL_d, point_loads, distributed_loads, load_factor, dynp, y_vals)[0]

    Ixx = MOI(0, wbox)[0]

    return -sigma_y(0, M, Ixx, wbox)[0]

def distspars(nspars):
    n = nspars - 2
    return [(0.2 + (0.45/(n+1))*(i+1), 1) for i in range(n)]

mos = 0
wingbox = design_options.option_new_2
start, end = 20, 40
curr = start
while True:
    wingbox["skin_thickness"] = curr*1e-3
    # wingbox["other_spars"] = distspars(curr)
    maxs = maxstress(wingbox)
    mos = (MAT["sigma_y"]*1e-6) / maxs
    print(curr, mos)
    if abs(mos - 1) < 0.01 or start == end:
        break
    if mos < 1:
        start = curr
        curr = (curr + end) / 2 # int(round((curr + end) / 2)) 
    else:
        end = curr
        curr =  (curr + start) / 2 # int(round((curr + start) / 2))

print("Final:", curr, mos)