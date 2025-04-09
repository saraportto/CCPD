#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

# TAMAÑO ARRAY A REPARTIR
LENGTH = 24

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
miRango = comm.rank
numProc = comm.size

# SOLO se ejecuta con número PAR de procesos
if numProc%2 != 0:
   if miRango == 0:
      print("ERROR: Tienes que usar un número par de procesos")
   quit()

if miRango == 0: # Proceso rango 0
   x = np.arange(LENGTH, dtype=np.float64) # x: vector 

else: # Resto de procesos
   x = None # x: None

# Todos crean y como array vacío de longitud LENGTH/numProc (carga equitativa entre procesos)
y = np.empty(int(LENGTH/numProc), dtype=np.float64)


# Proceso rango 0: PRINTEA       
if miRango == 0:
   print("Proceso %d/%d distribuyendo %d elementos" % (miRango, numProc, LENGTH))

# REALIZA SCATTER
comm.Scatter(x, y, root=0)
# x: QUÉ DATOS se envían (del root)
# y: A DÓNDE se envían (a todos los procesos del comunicador)
# root: FUENTE de los datos

# PRINTEA el resultado
print("Proceso %d/%d: " % (miRango, numProc), end='')
for elem in y:
   print("%d " % elem, end='')
print()


### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 6 ./07-Scatter.py
#
# Proceso 0/6 distribuyendo 24 elementos
# Proceso 0/6: 0 1 2 3
# Proceso 1/6: 4 5 6 7
# Proceso 2/6: 8 9 10 11
# Proceso 3/6: 12 13 14 15
# Proceso 4/6: 16 17 18 19
# Proceso 5/6: 20 21 22 23
### ---------------------- ###

