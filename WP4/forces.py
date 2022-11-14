import scipy as sp
from scipy import interpolate
from math import cos, sin


def torque_inboard(torque_outboard, moment_outboard, sweep_angle):
    return torque_outboard * cos(sweep_angle) + moment_outboard * sin(sweep_angle)


def moment_inboard(torque_outboard, moment_outboard, sweep_angle):
    return moment_outboard * cos(sweep_angle) - torque_outboard * sin(sweep_angle)


def dynamic_pressure(velocity, density):
    return 0.5 * density * velocity**2


def lift_per_span(dynamic_pressure, lift_coefficient, chord):
    return dynamic_pressure * lift_coefficient * chord


def lift_coefficient(lift, dynamic_pressure, surface_area):
    return lift / (dynamic_pressure * surface_area)


def drag_per_span(dynamic_pressure, drag_coefficient, chord):
    return dynamic_pressure * lift_coefficient * chord


def pitching_moment_per_span(dynamic_pressure, moment_coefficient, chord):
    return dynamic_pressure * moment_coefficient * chord**2


