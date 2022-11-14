import scipy as sp
import numpy as np
import XFLR
import ISA_calculator
import matplotlib.pyplot as plt 
from scipy import integrate
#Use XFLR.interpolater and XFLR.listtype
#Define denisty using ISa calculator
density = ISA_calculator.ISA(310,2)[2]
print(density)
#
velocity = 250
dyn_p = 0.5*density*velocity**2




def L_prime(y_pos):
    return(XFLR.interpolater(y_pos, XFLR.cl_lst)*dyn_p*XFLR.interpolater(y_pos, XFLR.c_lst))

def M_prime(y_pos):
    return(XFLR.interpolater(y_pos, XFLR.cm_lst)*dyn_p*XFLR.interpolater(y_pos, XFLR.c_lst)**2)

def D_prime(y_pos):
    return(XFLR.interpolater(y_pos, XFLR.cd_lst)*dyn_p*XFLR.interpolater(y_pos, XFLR.c_lst))
i=-22 
y_lst = []
D_lst=[]
L_lst = []
M_lst = []
while i<22:
    D_lst.append(D_prime(i))
    L_lst.append(L_prime(i))
    M_lst.append(M_prime(i))
    y_lst.append(i)
    i+=0.01

print(M_prime(10))
    
Lift = sp.integrate.quad(L_prime, -22, 22)
Drag = sp.integrate.quad(D_prime, -22, 22)
Moment =  sp.integrate.quad(M_prime, -22, 22)
print(Lift)
print(Drag)
print(Moment)