#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

# TAMAÑO DEL VECTOR
arraysize = 5

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
my_rank = comm.rank
num_processes = comm.size

# CREACIÓN DE vector
if my_rank == 0: # proceso 0: vector aleatorio
   vector = np.random.rand(arraysize)
   print("Vector en %d: " % my_rank, end='')
   for elem in vector:
      print("%.3f " % elem, end='')
   print()
else:  # otros procesos: vector ceros
   vector = np.zeros(arraysize)

# EJECUCIÓN DE BCAST
comm.Bcast(vector, root=0) 
# vector: QUÉ DATOS (root) / A DÓNDE (resto) se envían
# root: FUENTE de los datos

# MI RANGO 0 PRINTEA
if my_rank != 0:
   print("Proceso %d/%d: " % (my_rank,num_processes), end='')
   for elem in vector:
      print("%.3f " % elem, end='')
   print()


### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 4 ./05-Broadcast.py

# Vector en 0: 0.836 0.733 0.939 0.023 0.288
# Proceso 1/5: 0.836 0.733 0.939 0.023 0.288
# Proceso 3/5: 0.836 0.733 0.939 0.023 0.288
# Proceso 2/5: 0.836 0.733 0.939 0.023 0.288
# Proceso 4/5: 0.836 0.733 0.939 0.023 0.288

### ---------------------- ###


