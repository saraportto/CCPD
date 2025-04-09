#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

TAMBUFFER = 1000 # número de elementos por vector
FILENAME = "data.bin" # fichero a leer

# Info del COMUNICACDOR
comm = MPI.COMM_WORLD
numProcs = comm.Get_size()
miRango = comm.Get_rank()

# Solo con 3 procesos
if numProcs != 3:
    if miRango == 0:
        print("ERROR: el programa debe ser ejecutado con 3 procesos")
    quit()

# Creación VECTOR de datos
data = np.zeros(TAMBUFFER, dtype='d')

# Lectura en paralelo con MPI
mpi_file = MPI.File.Open(comm, FILENAME, MPI.MODE_RDONLY) # abre fichero
mpi_file.Set_view(miRango * TAMBUFFER * data.itemsize, MPI.DOUBLE) # establece la vista (1000 elementos desde la posicion especificada, en bytes)
mpi_file.Read_all(data) # lee el fichero en paralelo
mpi_file.Close() # cierra el fichero

# Cálculo de la MEDIA
mean = np.mean(data)
print(f"Vector {miRango}/{numProcs} - {TAMBUFFER} elementos: media = {mean:.3f}")
