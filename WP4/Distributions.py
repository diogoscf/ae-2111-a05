import XFLR
#import ISA_calculator
import matplotlib.pyplot as plt 
#Use XFLR.interpolater and XFLR.listtype
Density = 1
velocity = 10
dyn_p = 0.5*Density*velocity**2




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
    
plt.plot(y_lst, D_lst)
