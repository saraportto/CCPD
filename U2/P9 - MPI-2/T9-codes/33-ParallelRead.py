#! /usr/bin/env python
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

# DATA array (trocitos de datos) --> ceros
data = np.zeros(TAMBUFFER, dtype=np.int16)

# FICHEROS
mpi_file = MPI.File.Open(com, "Parallel2.data",MPI.MODE_RDONLY) # abre fichero: solo lectura
mpi_file.Set_view((2-miRango)*data.nbytes, MPI.SHORT) # vista: puntero de lectura distinto para cada proceso
mpi_file.Read(data) # lee el fichero y lo guarda en data
mpi_file.Close() # cierra el fichero

# PRINT
print("Proceso %d/%d lee:"%(miRango, numProcs), data)


# Proceso 0/3 lee: [ 8  9 10 11] ###
# Proceso 1/3 lee: [4 5 6 7]3-ParallelRead.py
# Proceso 2/3 lee: [0 1 2 3] 11]
# Proceso 1/3 lee: [4 5 6 7]
# Proceso 2/3 lee: [0 1 2 3]
### ------------------------- ###


