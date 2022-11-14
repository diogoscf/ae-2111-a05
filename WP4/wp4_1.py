from math import cos, sin


def torque_inboard(torque_outboard, moment_outboard, sweep_angle):
    return torque_outboard * cos(sweep_angle) + moment_outboard * sin(sweep_angle)


def moment_inboard(torque_outboard, moment_outboard, sweep_angle):
    return moment_outboard * cos(sweep_angle) - torque_outboard * sin(sweep_angle)
