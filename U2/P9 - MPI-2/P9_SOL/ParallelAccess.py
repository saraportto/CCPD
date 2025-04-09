#! /usr/bin/env python
from mpi4py import MPI
import numpy as np

numVectors = 3
vecSize = 1000

comm = MPI.COMM_WORLD
numProcs = comm.Get_size()
miRango = comm.Get_rank()

if numProcs!=numVectors:
   if miRango==0:
      print("ERROR: el programa debe ser ejecutado con %d procesos" % numVectors)
   quit()

data = np.zeros(vecSize)

mpi_file = MPI.File.Open(comm, "data.bin",MPI.MODE_RDONLY)
mpi_file.Set_view(miRango*data.nbytes, MPI.DOUBLE)
mpi_file.Read(data)
mpi_file.Close()

print("Vector %d/%d - %d elementos: media = %.3f "%(miRango, numProcs, len(data), np.mean(data) ))