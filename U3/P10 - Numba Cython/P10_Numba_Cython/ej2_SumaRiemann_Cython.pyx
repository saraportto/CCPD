cimport numpy
import numpy as np

def cython_riemann_sum(int n):
    cdef:
        double dx = (np.pi/2 - 0) / n
        double riemann_sum = 0

    for i in range(n):
        riemann_sum += np.sin((np.pi/2)*i/n) * dx
    return riemann_sum

def cython_riemann_sum_noloops(int n):
    cdef:
        double dx = (np.pi/2 - 0) / n
        double riemann_sum = 0
    
    riemann_sum += np.sin((np.pi/2)*0/n) * dx
    riemann_sum += np.sin((np.pi/2)*1/n) * dx
    riemann_sum += np.sin((np.pi/2)*2/n) * dx
    riemann_sum += np.sin((np.pi/2)*3/n) * dx
    riemann_sum += np.sin((np.pi/2)*4/n) * dx
    riemann_sum += np.sin((np.pi/2)*5/n) * dx
    riemann_sum += np.sin((np.pi/2)*6/n) * dx
    riemann_sum += np.sin((np.pi/2)*7/n) * dx
    riemann_sum += np.sin((np.pi/2)*8/n) * dx
    riemann_sum += np.sin((np.pi/2)*9/n) * dx
    return riemann_sum

