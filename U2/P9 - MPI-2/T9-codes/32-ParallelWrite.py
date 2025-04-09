#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

# TAMAÑO BUFFER
TAMBUFFER=4

# INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
numProcs = com.Get_size()
miRango = com.Get_rank()

# SOLO CON 3 PROCESOS
if numProcs!=3:
    if miRango==0:
        print("ERROR: el programa debe ser ejecutado con 3 procesos")
    quit()

# DATA array (trocitos de datos)
data = np.array([miRango*TAMBUFFER+i for i in range(TAMBUFFER)], dtype=np.int16)

# FICHEROS
mpi_file = MPI.File.Open(com, "Parallel2.data", MPI.MODE_WRONLY + MPI.MODE_CREATE) # abre fichero: escribe/crea fichero
mpi_file.Set_view(miRango*data.nbytes, MPI.SHORT) # vista desde donde escribe el proceso
mpi_file.Write(data) # cada proceso escribe su data en el fichero
mpi_file.Close() # cierra el fichero

# PRINT
print("Proceso %d/%d escribe:"%(miRango, numProcs), data)


### -------- CONSOLA --------- ###
# (mpi) $ mpirun -np 3 ./32-ParallelWrite.py
# Proceso 0/3 escribe: [0 1 2 3]
# Proceso 1/3 escribe: [4 5 6 7]
# Proceso 2/3 escribe: [ 8  9 10 11]

### ------------------------- ###


