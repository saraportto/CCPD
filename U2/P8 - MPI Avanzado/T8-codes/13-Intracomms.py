#!/usr/bin/env python

from mpi4py import MPI
import numpy as np

# nº etos array
num_data = 4

# INICIALIZACIÓN MPI
com = MPI.COMM_WORLD
miRango = com.rank
numProcs = com.size
miRangoSub = -9999

# CREACIÓN VECTOR con 4 datos
vector = np.zeros(num_data, dtype=int)

# SOLO con 5 procesos
if numProcs != 5:
   if miRango == 0:
      print("ERROR: lanzar el programa con 5 procesos")
   quit()

# CREACIÓN COMUNICADOR
grupo = com.Get_group() # obtener grupo de procesos
Rangos=[2,3,4] # rangos de procesos
grupoSub = grupo.Incl(Rangos) # crear subgrupo con rangos desde grupo
comSub = com.Create(grupoSub) # crear comunicador


# Para todos los procesos en el intracomunicador
if miRango in Rangos:
   miRangoSub = comSub.rank # obtiene rango
   if miRangoSub == 0:
      vector = np.random.randint(0, 10, num_data) # el de rango 0 genera el vector
   comSub.Bcast(vector, root=0) # todos ejecutan broadcast

print("Proceso %d/%d:" % (miRango,numProcs), vector)