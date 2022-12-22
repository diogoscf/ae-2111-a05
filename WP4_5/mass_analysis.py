from params import *
import design_options
from stresses import area
from stiffness import chord_y

import scipy as sp
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt

points = 300
halfspan = WING["span"] / 2
y_vals = np.linspace(0, halfspan, points)

def volume(wbox):
    ribs = wbox["ribs"]
    areas = [(r, area(r, wbox), area(r+1e-8, wbox)) for r in ribs]
    vol = sum([halfspan*(re - rs)*(area_s + area_e)/2 for (rs, _, area_s), (re, area_e, _) in zip(areas, areas[1:])])
    return vol   

if __name__ == "__main__":
    mass1 = volume(design_options.option_new_1)*MAT["density"]
    mass2 = volume(design_options.option_new_2)*MAT["density"]
    print(f"Option 1: {mass1} kg")
    print(f"Option 2: {mass2} kg")