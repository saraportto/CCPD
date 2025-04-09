#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
my_rank = comm.rank
num_processes = comm.size

num = np.zeros(1) # array de ceros de un elemento
num[0] = my_rank+1 # cada proceso le asigna su rango+1 a num

if my_rank == 0: # Proceso rango 0
    fact = np.zeros(1) # fact: array de ceros de un eto
else: # otros procesos
    fact = None # fact: None

# EJECUCIÓN DEL REDUCE
comm.Reduce(num, fact, op=MPI.PROD, root=0)
# num: lo que se envía (todos los procesos del comunicador)
# fact: array que recibe (en el root)
# op: operación a realizar (en este caso, producto)
# root: proceso que recibe el resultado de la operación

# Proceso rango 0: num[0] = 1*2*3*4*5 --> PRINTEA
if my_rank == 0:
    print("Proceso %d/%d: fact(%d)=%d" % (
        my_rank, num_processes, num_processes ,fact[0]))
    

### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 5 ./06-Reduce.py
# Proceso 0/5: fact(5)=120
### ---------------------- ###


