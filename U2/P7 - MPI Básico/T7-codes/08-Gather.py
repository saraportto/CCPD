#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

# LONGITUD DEL ARRAY A REUNIR
LENGTH = 16

# INICIALIZACIÓN MPI
comm = MPI.COMM_WORLD
miRango = comm.rank
numProc = comm.size


# SOLO se ejecuta si el número de procesos puede dividir LENGTH
if (LENGTH%numProc != 0):
   if miRango == 0:
      print("Tienes que usar un número de procesos divisor de",LENGTH)
   quit()

# CREACIÓN DEL ARRAY x para cada proceso (tamaño length/numProc)
x = np.arange(LENGTH/numProc*miRango, LENGTH/numProc*(miRango+1)) 
print("Proceso %d/%d: " % (miRango, numProc), end='')
print(x)

# Proceso rango 0
if miRango==0: 
   y = np.zeros(LENGTH) # y: array de ceros de longitud LENGTH
# Resto
else:
   y = None	# y: None

# REALIZACIÓN DEL GATHER
comm.Gather(x, y, root=0)
# x: QUÉ DATOS se envían (de todos los procesos)
# y: A DÓNDE se envían (al root)
# root: FUENTE de los datos

# Proceso 0 printea
if miRango == 0:
   print("El proceso 0 reunió los elementos:", y) 


### ------- CONSOLA ------- ###
# (mpi) $ mpirun -np 4 ./08-Gather.py

# Proceso 1/4: [4. 5. 6. 7.]
# Proceso 3/4: [12. 13. 14. 15.]
# Proceso 0/4: [0. 1. 2. 3.]
# Proceso 2/4: [ 8. 9. 10. 11.]
# El proceso 0 reunió los elementos: [ 0. 1.
# 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12.
# 13. 14. 15.]

### ---------------------- ###







