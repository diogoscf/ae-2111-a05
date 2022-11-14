import numpy as np
import scipy as sp 
from scipy import integrate 
import matplotlib.pyplot as plt 
from XFLR import interpolater

def f(y_pos): 
  return interpolater(y_pos, cl_lst)

estimatef,errorf = sp.integrate.quad(-f,0,21.79)
print(

