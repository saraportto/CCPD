#! /usr/bin/env python

import numpy as np
from mpi4py import MPI
import time

# INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
numProcs = com.Get_size()
miRango = com.Get_rank()

# SOLO CON 3 PROCESOS
if numProcs!=3:
    if miRango==0:
        print("ERROR: el programa debe ser ejecutado con 3 procesos")
    quit()

# Proceso 0 crea ventana con memoria compartida
if miRango == 0:
    a = np.arange(9, dtype=np.int16)
    print("Proceso",miRango,"comparto", a)
    window = MPI.Win.Create(a, comm=com)
else:
    window = MPI.Win.Create(None, comm=com)

# Proceso 1 lee ventana de proceso 0
if miRango == 1:
    b = 10 + np.arange(9, dtype=np.int16)
    window.Lock(0) # BLOQUEA 
    time.sleep(3)
    window.Put(b, target_rank=0) # escribe window del proceso 0 con b
    window.Unlock(0) # BLOQUEA


# LIBERA VENTANAS
window.Free() # libera
com.Barrier() # espera a que todos terminen

# PRINT
if miRango == 0:
    print("Proceso",miRango,"resultado", a)


### ------- CONSOLA --------- ###
# % mpirun -np 3 python 30-RMA-lock.py
# Proceso 0 comparto [0 1 2 3 4 5 6 7 8]
# Proceso 1 resultado [10 11 12 13 14 15 16 17 18]
# Proceso 0 resultado [10 11 12 13 14 15 16 17 18]

### ------------------------- ###


