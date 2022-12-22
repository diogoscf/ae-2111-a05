import numpy as np
import matplotlib.pyplot as plt
from math import pi
import scipy as sp
from scipy import interpolate
from params import *
from compression_failure import *
from design_options import *

STRINGER = { #current design
    "vertical_l": 60, #mm
    "horizontal_l": 60, #mm
    "thickness": 6, #mm
    "E_AL6061-T6": 68.9*10**9 #Pa
}

#critical sigma of segment at y/(b/2)
def crit_buckling_str(y,option):
    Ribs_pos=option["ribs"]
    Index=range(0,len(Ribs_pos))
    
    A=option["stringer_area"]*10**6 #mm^2
    vl=(5*A)**0.5 #mm
    t=A/(2*vl) #mm
    I= 1/12*t*vl**3 + t*vl*(0.5*vl)**2 #mm^4
    
    g=sp.interpolate.interp1d(Ribs_pos,Index,kind="next",fill_value="extrapolate")
    L= (Ribs_pos[int(g(y))]-Ribs_pos[int(g(y)-1)])*(WING["span"]*1000)/2 #mm
    E= STRINGER["E_AL6061-T6"] #Pa
    K=4 

    o_cr= (K*pi**2*E*I)/(L**2*A) *10**-6 #MPa
    return o_cr

#margin of safety
def mos(option):
    y_lst=[] #m
    sigma_y_lst=[]
    o_cr_lst=[]
    y=0
    dy=1/300
    for i in range(0,300):
        sigma_y_lst.append(sigma_y(y,option))
        o_cr_lst.append(crit_buckling_str(y,option))
        y_lst.append(y*WING["span"]/2)
        y=y+dy

    sigma_y_lst=np.array(sigma_y_lst)
    sigma_y_lst=np.delete(sigma_y_lst,0)
    o_app_lst=np.divide(sigma_y_lst,-1000000) #Mpa
    o_cr_lst=np.array(o_cr_lst) 
    o_cr_lst=np.delete(o_cr_lst,0) #Mpa

    m_of_s=np.divide(o_cr_lst,o_app_lst) #[-]
    return y_lst, m_of_s


def plot_m_of_s_current(): #one (current) design
    y_lst=np.delete(mos(WINGBOX)[0],0)
    
    plt.plot(y_lst,mos(WINGBOX)[1])
    plt.title("Margin of safety along the span")
    plt.ylabel("MoS [-]")
    plt.xlabel("y [m]")
    plt.ylim([0,4])
    plt.grid(True)

    plt.show()

def plot_m_of_s_old(): #three (old) designs
    y_lst=np.delete(mos(option_1)[0],0)
    
    plt.plot(y_lst,mos(option_1)[1],color='blue')
    plt.plot(y_lst,mos(option_2)[1],color='orange')
    plt.plot(y_lst,mos(option_3)[1],color='green')
    plt.title("Margin of safety along the span")
    plt.legend(('Design Option 1','Design Option 2','Design Option 3'))
    plt.ylabel("MoS [-]")
    plt.xlabel("y [m]")
    plt.ylim([0,4])
    plt.grid(True)

    plt.show()
    

#plot_m_of_s_old()

plot_m_of_s_current()
