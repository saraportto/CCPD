#!/usr/bin/env python
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
numProcs = comm.Get_size()
miRango = comm.Get_rank()
numElems = 1000
numVectors = 3
means = [0, 0.9, -1.2]
Verbose = True

if numProcs!=numVectors+1:
   if miRango==0:
      print("ERROR: el programa debe ser ejecutado con 4 procesos")
   quit()

if miRango != 0:
   miVector = np.random.normal(means[miRango-1], 1.0, size = numElems)

# Cabeza del vector generado por procesos 1 en adelante
if miRango != 0 and Verbose==True:
   print("P%d: %f %f" % (miRango, miVector[0], miVector[1]))

# TODO: crea el objeto ventana:
#   En el proceso 0 la ventana debe tener capacidad para todos los números y
#      se corresponde con un vector numpy llamado 'vec_mem'
#   El resto de procesos no contribuyen

# CREACIÓN OBJETO VENTANA
if miRango == 0: # proceso 0 crea la ventana
    vec_mem = np.zeros(numElems*numVectors, dtype='d')
    vec_desplazamiento = vec_mem.itemsize

else: # procesos 1,2,3 no contribuyen a la ventana
    vec_mem = None
    vec_desplazamiento = 1

vec_win = MPI.Win.Create(memory=vec_mem, disp_unit=vec_desplazamiento, comm=comm)

vec_win.Fence() # Sicronizar antes del Put

# TODO: los procesos con rango>=1 ponen sus datos en el objeto ventana
#   Ej: algo como win.Put(data, target_rank=0, target=pos)
#   escribe los datos 'data' en el proceso 0 a partir de la posición 'pos'

# PROCESOS 1,2,3 PONEN SUS DATOS EN LA VENTANA
if miRango != 0:
    pos = (miRango-1)*numElems
    vec_win.Put([miVector, MPI.DOUBLE], target_rank=0, target=pos)

vec_win.Fence() # Sincronizar despues del Put

# Cabezas de los vectores escritos en la ventana
if miRango==0 and Verbose==True:
   print("P0 vec1: %f %f" % (vec_mem[0], vec_mem[1]))
   print("P0 vec2: %f %f" % (vec_mem[numElems+0], vec_mem[numElems+1]))
   print("P0 vec3: %f %f" % (vec_mem[numElems*2+0], vec_mem[numElems*2+1]))

if miRango == 0:
    binary_file = open("data.bin", "wb")
    binary_file.write(vec_mem)
    binary_file.close()