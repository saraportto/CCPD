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


if miRango==0:
    vec_mem = np.zeros(numElems*numVectors)
    vec_disp = vec_mem.itemsize
else:
    vec_mem = None
    vec_disp = 1

win = MPI.Win.Create(vec_mem, vec_disp, comm=comm)

win.Fence()
if miRango==1:
   win.Put(miVector, target_rank=0, target=0)
if miRango==2:
   win.Put(miVector, target_rank=0, target=numElems)
if miRango==3:
   win.Put(miVector, target_rank=0, target=numElems*2)
win.Fence()

# Cabezas de los vectores escritos en la ventana
if miRango==0 and Verbose==True:
   print("P0 vec1: %f %f" % (vec_mem[0], vec_mem[1]))
   print("P0 vec2: %f %f" % (vec_mem[numElems+0], vec_mem[numElems+1]))
   print("P0 vec3: %f %f" % (vec_mem[numElems*2+0], vec_mem[numElems*2+1]))

if miRango == 0:
    binary_file = open("data.bin", "wb")
    binary_file.write(vec_mem)
    binary_file.close()