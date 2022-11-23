import scipy as sp
import numpy as np
import XFLR
import ISA
import matplotlib.pyplot as plt
from scipy import integrate
from math import cos, sin, asin, radians
import math

# Use XFLR.interpolater and XFLR.listtype
# Define denisty using ISa calculator
density = ISA.fl(310)[2]
# print(density)
#
velocity = 10
dyn_p = 0.5 * density * velocity**2
Wing_Surface = 189.92
AR = 10
e = 0.51
CD_0 = 0.028

# Defines function to calculate force/moment per unit span.
def L_prime_0(y_pos):
    return (
        XFLR.interpolater(y_pos, XFLR.cl_lst_0)
        * dyn_p
        * XFLR.interpolater(y_pos, XFLR.c_lst)
    )


def M_prime_0(y_pos):
    return (
        XFLR.interpolater(y_pos, XFLR.cm_lst_0)
        * dyn_p
        * XFLR.interpolater(y_pos, XFLR.c_lst) ** 2
    )


def D_prime_0(y_pos):
    return (
        XFLR.interpolater(y_pos, XFLR.cd_lst_0)
        * dyn_p
        * XFLR.interpolater(y_pos, XFLR.c_lst)
    )


def L_prime_10(y_pos):
    return (
        XFLR.interpolater(y_pos, XFLR.cl_lst_10)
        * dyn_p
        * XFLR.interpolater(y_pos, XFLR.c_lst)
    )


def M_prime_10(y_pos):
    return (
        XFLR.interpolater(y_pos, XFLR.cm_lst_10)
        * dyn_p
        * XFLR.interpolater(y_pos, XFLR.c_lst) ** 2
    )


def D_prime_10(y_pos):
    return (
        XFLR.interpolater(y_pos, XFLR.cd_lst_10)
        * dyn_p
        * XFLR.interpolater(y_pos, XFLR.c_lst)
    )


# This is used for plotting to check results
# i=-22
# y_lst = []
# D_lst=[]
# L_lst = []
# M_lst = []
# while i<22:
#    D_lst.append(D_prime(i))
#    L_lst.append(L_prime(i))
#    M_lst.append(M_prime(i))
#    y_lst.append(i)
#    i+=0.01

# print(M_prime(10))
# Integrates to obtain total values over wing
# Lift_0 = sp.integrate.quad(L_prime_0, -22, 22)
# Drag_0 = sp.integrate.quad(D_prime_0, -22, 22)
Moment_0 = sp.integrate.quad(M_prime_0, -21.79, 21.79)
# Calculates Coefficients
CL_0 = 0.32024
CD_0 = 0.003271
CM_0 = Moment_0[0] / (dyn_p * Wing_Surface * 4.355)

# Lift_10 = sp.integrate.quad(L_prime_10, -22, 22)
# Drag_10 = sp.integrate.quad(D_prime_10, -22, 22)
Moment_10 = sp.integrate.quad(M_prime_10, -21.79, 21.79)

CL_10 = 1.1154
CD_10 = 0.038375
CM_10 = Moment_10[0] / (dyn_p * Wing_Surface * 4.355)
# Uncomment these to check values or use variable explorer
# print (CL_0)
# print (CD_0)
# print (CM_0)
# print (CL_10)
# print (CD_10)
# print (CM_10)


# Functions to determine lift distribution and AoA of specific CL
def lift_distribution_specific_flight_regime(CL_d):
    cl_d_lst = XFLR.cl_lst_0 + ((CL_d - CL_0) / (CL_10 - CL_0)) * (
        XFLR.cl_lst_10 - XFLR.cl_lst_0
    )
    return cl_d_lst

def AOA_specific_flight_regime(CL_d):
    return asin((CL_d - CL_0) / (CL_10 - CL_0) * sin(radians(10))) * 57.3


# Determines Cd dist at given CD
def drag_distribution_specific_flight_regime(CD_d):
    cd_d_lst = XFLR.cd_lst_0 + ((CD_d - CD_0) / (CD_10 - CD_0)) * (
        XFLR.cd_lst_10 - XFLR.cd_lst_0
    )
    return cd_d_lst


# determines Cm dist at given CM
def moment_distribution_specific_flight_regime(CM_d):
    cm_d_lst = XFLR.cm_lst_0 + ((CM_d - CM_0) / (CM_10 - CM_0)) * (
        XFLR.cm_lst_10 - XFLR.cm_lst_0
    )
    return cm_d_lst




# print(AOA_specific_flight_regime(1)*57.3)
# Function to plot a lift distribution of any given CL
def Plot_lift_distribution(CL_d):
    y_pos = np.linspace(0, 21.79, 100)
    plt.plot(
        y_pos, XFLR.interpolater(y_pos, lift_distribution_specific_flight_regime(CL_d))
    )
    plt.xlabel("y(m)")
    plt.ylabel("Cl(-)")
    plt.title("Lift distribution")
    
def Plot_drag_distribution(CD_d):
    y_pos = np.linspace(-21.79, 21.79, 100)
    plt.plot(
        y_pos, XFLR.interpolater(y_pos, drag_distribution_specific_flight_regime(CD_d))
    )


def Plot_moment_distribution(CM_d):
    y_pos = np.linspace(-21.79, 21.79, 100)
    plt.plot(
        y_pos,
        XFLR.interpolater(y_pos, moment_distribution_specific_flight_regime(CM_d)),
    )


# Gives Cl at any y position for any given CL
def Cl_at_y(CL_d, y_pos):
    Cl = XFLR.interpolater(y_pos, lift_distribution_specific_flight_regime(CL_d))
    return Cl


# Specific Cd at position at given CD
def Cd_at_y(CD_d, y_pos):
    Cd = XFLR.interpolater(y_pos, drag_distribution_specific_flight_regime(CD_d))
    return Cd


# L_prime for any given CL and position
def Cm_at_y(CM_d, y_pos):
    Cm = XFLR.interpolater(y_pos, moment_distribution_specific_flight_regime(CM_d))
    return Cm


def L_prime(CL_d, y_pos, dyn_p):
    return Cl_at_y(CL_d, y_pos) * dyn_p * XFLR.interpolater(y_pos, XFLR.c_lst)


# D_prime for any given CD and position
def D_prime(CD_d, y_pos, dyn_p):
    return Cd_at_y(CD_d, y_pos) * dyn_p * XFLR.interpolater(y_pos, XFLR.c_lst)


# M_prime for any given CM and position
def M_prime(CM_d, y_pos, dyn_p):
    return Cm_at_y(CM_d, y_pos) * dyn_p * XFLR.interpolater(y_pos, XFLR.c_lst) ** 2


# N_prime for any given CL, CD and position
def N_prime(CL_d, CD_d, y_pos, dyn_p):
    return L_prime(CL_d, y_pos, dyn_p) * cos(
        radians(AOA_specific_flight_regime(CL_d))
    ) + D_prime(CD_d, y_pos, dyn_p) * sin(radians(AOA_specific_flight_regime(CL_d)))


# Plots shear distribution
def plot_Shear_distribution(CL_d, dyn_p):
    CD_d = CD_0 + CL_d**2 / (math.pi * AR * e)
    y_pos = np.linspace(0, 21.79, 1000)
    plt.plot(y_pos, N_prime(CL_d, CD_d, y_pos, dyn_p))


# Plots moment distributions
def plot_Moment_distribution(CM_d, dyn_p):
    y_pos = np.linspace(0, 21.79, 1000)
    plt.plot(y_pos, M_prime(CM_d, y_pos, dyn_p))


# Makesa Shear force diagram. P is a point load, P_y_pos is it's position along the wingspan
def plot_Shear_diagram(CL_d, dyn_p, P, P_y_pos):
    CD_d = CD_0 + CL_d**2/(math.pi*AR*e)
    y_pos = 0
    y_lst= []
    Shear=[]
    while  y_pos <= P_y_pos:
        
        Shear_value=sp.integrate.quad(lambda y: N_prime(CL_d, CD_d, y, dyn_p), y_pos, 21.79)[0]-P
        Shear.append(Shear_value)
        y_lst.append(y_pos)
        y_pos+=0.1
    while  y_pos <= 21.8 and y_pos >P_y_pos:
        
        Shear_value=sp.integrate.quad(lambda y: N_prime(CL_d, CD_d, y, dyn_p), y_pos, 21.79)[0]
        Shear.append(Shear_value)
        y_lst.append(y_pos)
        y_pos+=0.1
    
    plt.plot(y_lst, Shear)
    plt.show()
    print(Shear[-1])
    print(Shear[0])
    return(Shear)
#def plot_Shear_diagram2(CL_d, dyn_p):
    CD_d = CD_0 + CL_d**2/(math.pi*AR*e)
    y_pos = 0
    y_lst = []
    Shear = []
    while y_pos <= P_y_pos:

        Shear_value = (
            sp.integrate.quad(lambda y: N_prime(CL_d, CD_d, y, dyn_p), y_pos, 21.79)[0]
            - P
        )
        Shear.append(Shear_value)
        y_lst.append(y_pos)
        y_pos += 0.1
    while y_pos <= 21.8 and y_pos > P_y_pos:

        Shear_value = sp.integrate.quad(
            lambda y: N_prime(CL_d, CD_d, y, dyn_p), y_pos, 21.79
        )[0]
        Shear.append(Shear_value)
        y_lst.append(y_pos)
        y_pos += 0.1

    plt.plot(y_lst, Shear)
    plt.show()
    # print(Shear[-1])
    return Shear


def plot_Shear_diagram2(CL_d, dyn_p):
    CD_d = CD_0 + CL_d**2 / (math.pi * AR * e)
    y_pos = 0
    y_lst = []
    Shear = []
    while y_pos <= 21.8:

        if y_pos < 10:
            Shear.append(N_prime(CL_d, CD_d, y_pos, dyn_p))

        else:
            Shear.append((N_prime(CL_d, CD_d, y_pos, dyn_p)) + 10000)
        y_lst.append(y_pos)
        y_pos += 0.1
    plt.plot(y_lst, Shear)
    return Shear


# plot_Shear_diagram(1, 10000, -300000, 10)


def make_y_list():
    i = 0
    y_lst = []
    y = 0
    while i < 218:
        y_lst.append(y)
        y += 0.1
        i += 1
    return y_lst


def interpolater2(y_pos, listtype):
    y_lst = make_y_list()
    value = sp.interpolate.interp1d(
        y_lst, listtype, kind="cubic", fill_value="extrapolate"
    )
    value = value(abs(y_pos))
    return value


# Plots moment diagram
def plot_Moment_diagram(CL_d, dyn_p, P, P_y_pos, M, M_y_pos):
    y_pos = 0
    y_lst2 = []
    Moment = []
    Shear_list = plot_Shear_diagram(CL_d, dyn_p, P, P_y_pos)
    while y_pos <= M_y_pos:
        Moment_value = (
            sp.integrate.quad(lambda y: interpolater2(y, Shear_list), y_pos, 21.79)[0]
            - M
        )
        y_pos += 0.1
        y_lst2.append(y_pos)
        Moment.append(Moment_value)
    while y_pos > M_y_pos and y_pos <= 21.8:
        Moment_value = sp.integrate.quad(
            lambda y: interpolater2(y, Shear_list), y_pos, 21.79
        )[0]
        y_pos += 0.1
        y_lst2.append(y_pos)
        Moment.append(Moment_value)
    plt.plot(y_lst2, Moment)
    print(Moment[-1])
    print(Moment[0])
    
def plot_normal_diagram (Thrust, Position, Angle):
    y_pos=0
    y_lst2=[] 
    Compression_lst = []
    while y_pos <= Position:
        y_pos+=0.1
        y_lst2.append(y_pos)
        Compression_lst.append(-Thrust*sin(radians(Angle)))
    while y_pos >Position and y_pos <=21.8 :
        y_pos+=0.1
        y_lst2.append(y_pos)
        Compression_lst.append(0)
    plt.plot(y_lst2, Compression_lst)
        
    
Plot_lift_distribution(1)

