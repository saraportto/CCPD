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

# DATA arrays
data = np.zeros(4, dtype=np.int16) # inicializa array ceros 4 etos
data_aux = np.zeros(1, dtype=np.int16) # inicializa array ceros 1 eto


# FICHEROS
mpi_file = MPI.File.Open(com, "Parallel2.data",MPI.MODE_RDONLY) # abre fichero: solo lectura
data_type = MPI.SHORT.Create_vector(4, 1, 3) # vector 4 bloques, bloque 1 eto, desplazamiento 3 etos
data_type.Commit() # commit
mpi_file.Set_view(miRango*data_aux.nbytes, data_type) # vista: puntero de lectura distinto para cada proceso
mpi_file.Read(data) # lee el fichero y lo guarda en data
mpi_file.Close() # cierra el fichero

# PRINT
print("Proceso %d/%d lee:"%(miRango, numProcs), data)


### ------- CONSOLA --------- ###
# % mpirun -np 3 python 34-ParallelReadNonCont.py
# Proceso 0/3 lee: [ 8  9 10 11]
# Proceso 1/3 lee: [4 5 6 7]
# Proceso 2/3 lee: [0 1 2 3]
### ------------------------- ###



